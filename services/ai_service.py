from google import genai
from google.genai import types
import os
import json
import json as _json
from pathlib import Path
import time as _time

from dotenv import load_dotenv

# region agent log
try:
    _data = {
        "sessionId": "4da1d4",
        "runId": "pre-fix-import",
        "hypothesisId": "H2",
        "location": "services/ai_service.py:load_env_before",
        "message": "Before loading env for GEMINI_API_KEY",
        "data": {
            "cwd": os.getcwd(),
            "env_local_exists": Path(".env.local").is_file(),
        },
        "timestamp": int(_time.time() * 1000),
    }
    with open("debug-4da1d4.log", "a", encoding="utf-8") as _f:
        _f.write(_json.dumps(_data) + "\n")
except Exception:
    pass
# endregion

load_dotenv(".env.local")

api_key = os.getenv("GEMINI_API_KEY")

# region agent log
try:
    _data = {
        "sessionId": "4da1d4",
        "runId": "pre-fix-import",
        "hypothesisId": "H2",
        "location": "services/ai_service.py:load_env_after",
        "message": "After loading env for GEMINI_API_KEY",
        "data": {
            "has_api_key": api_key is not None,
        },
        "timestamp": int(_time.time() * 1000),
    }
    with open("debug-4da1d4.log", "a", encoding="utf-8") as _f:
        _f.write(_json.dumps(_data) + "\n")
except Exception:
    pass
# endregion

client = genai.Client(api_key=api_key)


def extract_assignments(markdown_text):
    model_name = "gemini-3.1-flash-lite-preview"

    prompt = f"Extract assignments (quizzes, homework, exams, etc.) as JSON from the following text: {markdown_text}"

    # region agent log
    try:
        _data = {
            "sessionId": "4da1d4",
            "runId": "pre-fix-gemini",
            "hypothesisId": "H3",
            "location": "services/ai_service.py:before_generate",
            "message": "Before calling Gemini generate_content",
            "data": {
                "model_name": model_name,
                "markdown_length": len(markdown_text) if isinstance(markdown_text, str) else None,
            },
            "timestamp": int(_time.time() * 1000),
        }
        with open("debug-4da1d4.log", "a", encoding="utf-8") as _f:
            _f.write(_json.dumps(_data) + "\n")
    except Exception:
        pass
    # endregion

    response = client.models.generate_content(model=model_name, contents=prompt)

    # region agent log
    try:
        _data = {
            "sessionId": "4da1d4",
            "runId": "pre-fix-gemini",
            "hypothesisId": "H3",
            "location": "services/ai_service.py:after_generate",
            "message": "After calling Gemini generate_content",
            "data": {
                "has_text": hasattr(response, "text"),
            },
            "timestamp": int(_time.time() * 1000),
        }
        with open("debug-4da1d4.log", "a", encoding="utf-8") as _f:
            _f.write(_json.dumps(_data) + "\n")
    except Exception:
        pass
    # endregion

    return json.loads(response.text.strip("`").replace("json", ""))