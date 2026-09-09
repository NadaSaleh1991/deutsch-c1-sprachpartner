const setupView = document.getElementById("setup-view");
const sessionView = document.getElementById("session-view");
const feedbackView = document.getElementById("feedback-view");
const scenarioGrid = document.getElementById("scenario-grid");
const modeSelect = document.getElementById("mode-select");
const nativeLanguageInput = document.getElementById("native-language");
const sessionTitle = document.getElementById("session-title");
const sessionGoal = document.getElementById("session-goal");
const statusIndicator = document.getElementById("status-indicator");
const transcriptEl = document.getElementById("transcript");
const endSessionBtn = document.getElementById("end-session-btn");
const feedbackContent = document.getElementById("feedback-content");
const restartBtn = document.getElementById("restart-btn");
const errorBanner = document.getElementById("error-banner");

let scenarios = [];
let currentScenario = null;
let ws = null;
let micStream = null;
let micContext = null;
let micWorkletNode = null;
let playbackContext = null;
let nextPlayTime = 0;
let transcript = [];
let speakingTimeout = null;

function showView(view) {
  for (const v of [setupView, sessionView, feedbackView]) v.classList.add("hidden");
  view.classList.remove("hidden");
}

function showError(message) {
  errorBanner.textContent = message;
  errorBanner.classList.remove("hidden");
  setTimeout(() => errorBanner.classList.add("hidden"), 6000);
}

async function loadScenarios() {
  const res = await fetch("/api/scenarios");
  scenarios = await res.json();
  scenarioGrid.innerHTML = "";
  for (const s of scenarios) {
    const card = document.createElement("div");
    card.className = "scenario-card";
    card.innerHTML = `
      <div class="emoji">${s.emoji}</div>
      <h3>${s.title}</h3>
      <p>${s.setting}</p>
      <p class="goal">🎯 ${s.goal}</p>
    `;
    card.addEventListener("click", () => startSession(s));
    scenarioGrid.appendChild(card);
  }
}

async function startSession(scenario) {
  currentScenario = scenario;
  transcript = [];
  transcriptEl.innerHTML = "";
  sessionTitle.textContent = `${scenario.emoji} ${scenario.title}`;
  sessionGoal.textContent = `Ziel: ${scenario.goal}`;
  statusIndicator.textContent = "Verbindung wird aufgebaut …";
  statusIndicator.className = "status-indicator";
  showView(sessionView);

  try {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (err) {
    showError("Mikrofonzugriff wurde verweigert. Bitte erlaube den Zugriff und versuche es erneut.");
    showView(setupView);
    return;
  }

  const protocol = location.protocol === "https:" ? "wss:" : "ws:";
  ws = new WebSocket(`${protocol}//${location.host}/ws/session`);
  ws.binaryType = "arraybuffer";

  ws.onopen = async () => {
    ws.send(JSON.stringify({
      type: "start",
      scenario_id: scenario.id,
      mode: modeSelect.value,
      native_language: nativeLanguageInput.value || "Englisch",
    }));
    await startMic();
    statusIndicator.textContent = "🎤 Du bist dran — sprich einfach los.";
    statusIndicator.className = "status-indicator listening";
  };

  ws.onmessage = (event) => {
    if (typeof event.data === "string") {
      const msg = JSON.parse(event.data);
      if (msg.type === "transcript") {
        addBubble(msg.role, msg.text);
      } else if (msg.type === "turn_complete") {
        statusIndicator.textContent = "🎤 Du bist dran — sprich einfach los.";
        statusIndicator.className = "status-indicator listening";
      }
    } else {
      playAudioChunk(event.data);
      statusIndicator.textContent = "🔊 Gesprächspartner spricht …";
      statusIndicator.className = "status-indicator speaking";
    }
  };

  ws.onerror = () => showError("Verbindungsfehler zum Server.");
  ws.onclose = () => stopMic();
}

async function startMic() {
  micContext = new AudioContext({ sampleRate: 16000 });
  await micContext.audioWorklet.addModule("/audio-processor.js");
  const source = micContext.createMediaStreamSource(micStream);
  micWorkletNode = new AudioWorkletNode(micContext, "pcm-recorder-processor");
  micWorkletNode.port.onmessage = (event) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(event.data);
    }
  };
  source.connect(micWorkletNode);
}

function stopMic() {
  if (micStream) micStream.getTracks().forEach((t) => t.stop());
  if (micContext) micContext.close();
  micStream = null;
  micContext = null;
  micWorkletNode = null;
}

function playAudioChunk(arrayBuffer) {
  if (!playbackContext) {
    playbackContext = new AudioContext({ sampleRate: 24000 });
    nextPlayTime = playbackContext.currentTime;
  }
  const int16 = new Int16Array(arrayBuffer);
  const float32 = new Float32Array(int16.length);
  for (let i = 0; i < int16.length; i++) float32[i] = int16[i] / 32768;

  const buffer = playbackContext.createBuffer(1, float32.length, 24000);
  buffer.copyToChannel(float32, 0);

  const source = playbackContext.createBufferSource();
  source.buffer = buffer;
  source.connect(playbackContext.destination);

  const startAt = Math.max(nextPlayTime, playbackContext.currentTime);
  source.start(startAt);
  nextPlayTime = startAt + buffer.duration;
}

function addBubble(role, text) {
  transcript.push({ role, text });
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  transcriptEl.appendChild(bubble);
  transcriptEl.scrollTop = transcriptEl.scrollHeight;
}

async function endSession() {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: "end" }));
    ws.close();
  }
  stopMic();
  statusIndicator.textContent = "Auswertung wird erstellt …";
  showView(feedbackView);
  feedbackContent.innerHTML = "<p class='muted'>Einen Moment …</p>";

  try {
    const res = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        scenario_id: currentScenario.id,
        native_language: nativeLanguageInput.value || "Englisch",
        transcript,
      }),
    });
    if (!res.ok) throw new Error("Feedback request failed");
    renderFeedback(await res.json());
  } catch (err) {
    feedbackContent.innerHTML = "<p class='muted'>Auswertung konnte nicht erstellt werden.</p>";
    showError("Die Auswertung konnte nicht geladen werden.");
  }
}

function renderFeedback(fb) {
  const scoreLabels = {
    wortschatz: "Wortschatz",
    grammatik: "Grammatik",
    fluessigkeit_kohaerenz: "Flüssigkeit & Kohärenz",
    register_angemessenheit: "Register / Angemessenheit",
    aufgabenerfuellung: "Aufgabenerfüllung",
  };

  const scoresHtml = Object.entries(fb.scores || {})
    .map(([key, value]) => `
      <div class="score-row">
        <div class="score-label">${scoreLabels[key] || key}</div>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:${(value / 6) * 100}%"></div></div>
        <div>${value}/6</div>
      </div>
    `).join("");

  const staerkenHtml = (fb.staerken || []).map((s) => `<li>${s}</li>`).join("");

  const verbesserungenHtml = (fb.verbesserungen || []).map((v) => `
    <div class="correction-item">
      <div class="wrong">${v.fehler_zitat}</div>
      <div class="right">${v.korrektur}</div>
      <div class="muted">${v.erklaerung}</div>
    </div>
  `).join("");

  const naechsteHtml = (fb.naechste_schritte || []).map((s) => `<li>${s}</li>`).join("");

  feedbackContent.innerHTML = `
    <div class="feedback-card">
      <span class="cefr-badge">Geschätztes Niveau: ${fb.cefr_einschaetzung || "—"}</span>
      <p class="muted">${fb.aufgabe_erreicht ? "✅ Gesprächsziel erreicht" : "⚠️ Gesprächsziel nicht ganz erreicht"}</p>
    </div>
    <div class="feedback-card">
      <h3>Bewertung</h3>
      ${scoresHtml}
    </div>
    <div class="feedback-card">
      <h3>Stärken</h3>
      <ul>${staerkenHtml}</ul>
    </div>
    <div class="feedback-card">
      <h3>Verbesserungsvorschläge</h3>
      ${verbesserungenHtml}
    </div>
    <div class="feedback-card">
      <h3>Nächste Schritte</h3>
      <ul>${naechsteHtml}</ul>
    </div>
  `;
}

endSessionBtn.addEventListener("click", endSession);
restartBtn.addEventListener("click", () => showView(setupView));

loadScenarios();
