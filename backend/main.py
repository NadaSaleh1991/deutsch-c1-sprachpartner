import asyncio
import json
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from pydantic import BaseModel

from backend.config import GEMINI_API_KEY, GEMINI_LIVE_MODEL, GEMINI_TEXT_MODEL, GEMINI_VOICE
from backend.prompts import build_feedback_prompt, build_live_system_instruction
from backend.scenarios import SCENARIOS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("german-c1-tutor")

app = FastAPI(title="German C1 Immersion Tutor")
client = genai.Client(api_key=GEMINI_API_KEY)


@app.get("/api/scenarios")
async def list_scenarios():
    return SCENARIOS


class FeedbackRequest(BaseModel):
    scenario_id: str
    native_language: str
    transcript: list[dict]


@app.post("/api/feedback")
async def feedback(req: FeedbackRequest):
    prompt = build_feedback_prompt(req.scenario_id, req.transcript, req.native_language)
    response = await client.aio.models.generate_content(
        model=GEMINI_TEXT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(response.text)


@app.websocket("/ws/session")
async def live_session(websocket: WebSocket):
    await websocket.accept()

    try:
        init_raw = await websocket.receive_text()
        init = json.loads(init_raw)
        system_instruction = build_live_system_instruction(
            scenario_id=init["scenario_id"],
            mode=init["mode"],
            native_language=init["native_language"],
        )
    except (WebSocketDisconnect, KeyError, json.JSONDecodeError, ValueError) as exc:
        logger.warning("Bad session init: %s", exc)
        await websocket.close(code=1008)
        return

    live_config = types.LiveConnectConfig(
        response_modalities=[types.Modality.AUDIO],
        system_instruction=types.Content(parts=[types.Part(text=system_instruction)]),
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=GEMINI_VOICE)
            )
        ),
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
    )

    try:
        async with client.aio.live.connect(model=GEMINI_LIVE_MODEL, config=live_config) as session:

            async def client_to_gemini():
                while True:
                    message = await websocket.receive()
                    if message.get("type") == "websocket.disconnect":
                        return
                    if message.get("bytes") is not None:
                        await session.send_realtime_input(
                            audio=types.Blob(
                                data=message["bytes"], mime_type="audio/pcm;rate=16000"
                            )
                        )
                    elif message.get("text") is not None:
                        payload = json.loads(message["text"])
                        if payload.get("type") == "end":
                            return

            async def gemini_to_client():
                async for response in session.receive():
                    server_content = response.server_content
                    if server_content is None:
                        continue

                    if server_content.model_turn:
                        for part in server_content.model_turn.parts:
                            if part.inline_data and part.inline_data.data:
                                await websocket.send_bytes(part.inline_data.data)

                    if server_content.input_transcription and server_content.input_transcription.text:
                        await websocket.send_text(json.dumps({
                            "type": "transcript",
                            "role": "student",
                            "text": server_content.input_transcription.text,
                        }))

                    if server_content.output_transcription and server_content.output_transcription.text:
                        await websocket.send_text(json.dumps({
                            "type": "transcript",
                            "role": "tutor",
                            "text": server_content.output_transcription.text,
                        }))

                    if server_content.turn_complete:
                        await websocket.send_text(json.dumps({"type": "turn_complete"}))

            client_task = asyncio.create_task(client_to_gemini())
            gemini_task = asyncio.create_task(gemini_to_client())
            done, pending = await asyncio.wait(
                {client_task, gemini_task}, return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
            for task in done:
                exc = task.exception()
                if exc:
                    raise exc

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception:
        logger.exception("Live session error")
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            pass


app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def index():
    return FileResponse("static/index.html")
