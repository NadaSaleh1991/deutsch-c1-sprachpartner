import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Live (voice) model used for the roleplay conversation.
# Check https://ai.google.dev/gemini-api/docs/live-api for the current model id
# if this one has been retired/renamed.
GEMINI_LIVE_MODEL = os.environ.get("GEMINI_LIVE_MODEL", "gemini-3.1-flash-live-preview")

# Plain text model used for the end-of-session CEFR feedback report.
GEMINI_TEXT_MODEL = os.environ.get("GEMINI_TEXT_MODEL", "gemini-2.5-flash")

# Voice used by the AI persona (see Live API docs for available prebuilt voices).
GEMINI_VOICE = os.environ.get("GEMINI_VOICE", "Kore")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key "
        "(free at https://aistudio.google.com/apikey)."
    )
