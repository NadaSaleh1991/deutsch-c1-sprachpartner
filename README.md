# Deutsch C1 Sprachpartner

An immersive, voice-based German tutor for **C1-level** learners. You pick a
realistic scenario (negotiating rent reduction, a salary negotiation, a
seminar debate, a job interview for a leadership role, ...), talk to an AI
persona out loud in German, and get a CEFR-referenced performance report at
the end.

## How it works

```
Browser (mic)                FastAPI backend                 Gemini Live API
─────────────                ────────────────                ────────────────
AudioWorklet     --PCM16-->  WebSocket relay    --audio-->    gemini-*-live-preview
captures mic                 (backend/main.py)  <--audio--    (native speech-to-speech,
16kHz mono                                                     server-side VAD, barge-in)
                                    |
                              transcript accumulated
                                    |
                                    v
                        POST /api/feedback -> Gemini text model
                        -> CEFR-based JSON scoring report
```

- **Backend** (`backend/`): FastAPI. `main.py` opens a Gemini Live session per
  browser connection and relays raw audio bytes both ways over a WebSocket.
  It never touches the audio itself — Gemini handles turn-taking,
  interruption ("barge-in"), and speech synthesis natively.
- **Scenarios** (`backend/scenarios.py`): 8 C1-appropriate roleplay
  situations, each with a persona, setting, learner goal, register, and key
  phrases (*Redemittel*).
- **Prompts** (`backend/prompts.py`): builds the Live API system instruction
  (persona + mode rules) and the end-of-session feedback prompt.
- **Frontend** (`static/`): no build step — vanilla JS, Web Audio API +
  AudioWorklet for mic capture/playback, plain WebSocket.

## Two modes

- **Immersiv**: the AI never breaks character or corrects you — pure
  conversation practice.
- **Lehrer-Modus**: the AI occasionally drops a one-line correction (in your
  native language) after a mistake, then continues the scene in German.

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

copy .env.example .env
# then edit .env and paste your key
```

Get a **free** API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — no credit card required for the free tier.

Run it:

```bash
uvicorn backend.main:app --reload
```

Open http://localhost:8000, allow microphone access, pick a scenario, and talk.

## Is this free?

Yes, for portfolio/demo use. The Live API's native-audio model has a free
tier through AI Studio (rate-limited). Paid Live audio pricing is roughly
**$0.005/min input, $0.018/min output** — a 5-minute practice session costs a
few cents. The end-of-session feedback call uses a cheap text model
(`gemini-2.5-flash`), which is effectively free at this scale.

If you deploy this publicly, add rate limiting per IP/session before sharing
the link widely — nothing here does that by default.

## Why not a fully local/open-source stack?

That would mean chaining Whisper (STT) → a local LLM → a TTS model
(e.g. Kokoro) yourself, with no built-in interruption handling. It's very
doable, but it wants a real GPU for low-latency, natural-feeling
conversation. This machine's GPUs (Intel HD 5500 / AMD Radeon R5 M255, no
CUDA) aren't suited to that, so this project uses Gemini's hosted Live API
instead — it needs nothing more than a browser and an API key, which also
makes it trivial for anyone to clone and run.

## Scenarios included

| Scenario | Register |
|---|---|
| 🏚️ Mietminderung wegen Schimmel | formal, assertive |
| 💼 Gehaltsverhandlung | formal, persuasive |
| 🏛️ Widerspruch beim Bürgeramt | bureaucratic German |
| 🩺 Zweitmeinung beim Facharzt | formal, medical |
| 🎓 Seminardiskussion: Digitalisierung | academic, argumentative |
| 📦 Beschwerde beim Kundenservice | formal, complaint |
| 🔑 Wohnungsübergabe aushandeln | formal, conflict |
| 🧑‍💼 Vorstellungsgespräch: Führungsposition | formal, professional |

## Known limitations

- Live API model ids change over time — if the default in `.env.example`
  stops working, check [ai.google.dev/gemini-api/docs/live-api](https://ai.google.dev/gemini-api/docs/live-api)
  for the current one.
- Feedback quality depends on how well the Live API's transcription captures
  the learner's turns; heavy background noise will degrade both the
  conversation and the report.
- No persistence — sessions and transcripts live only in the browser tab.
