import json
import logging
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv(".env.local")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key or not api_key.strip():
    raise RuntimeError("GEMINI_API_KEY is not set in environment")

client = genai.Client(api_key=api_key)
logger = logging.getLogger(__name__)

# Retry config for transient API errors
MAX_RETRIES = 3
RETRY_DELAY_SEC = 2


def extract_assignments(markdown_text: str) -> dict:
    model_name = "gemini-3.1-flash-lite-preview"

    prompt = f"""
            You are an academic data engineer. Extract all assignments, quizzes, and exams from the syllabus.
            Return ONLY a JSON array.

            TIMEZONE & LOCALIZATION RULES:
            1. SCHOOL IDENTIFICATION: Identify the school/university from the syllabus text.
            2. TIMEZONE DETECTION: Determine the exact IANA Timezone ID for that school (e.g., 'America/New_York' for CWRU, 'America/Chicago' for UChicago).
            3. TIMED EVENTS: If a specific clock time is mentioned (e.g., 2:00 PM), return it in "YYYY-MM-DDTHH:MM:SS" format.
            4. ALL-DAY EVENTS: If NO time is mentioned, return ONLY "YYYY-MM-DD".
            5. DURATION: If an end time is missing, set it to 1 hour after the start time.

            JSON STRUCTURE:

            FOR GIVEN TIME:
            {{
            "timezone": "IANA_TIMEZONE_ID",
            "assignments": [
                {{
                "summary": "Midterm Exam",
                "start": "2026-03-24T14:30:00",
                "end": "2026-03-24T15:30:00",
                "description": "Chapters 1-5"
                }}
            ]
            }}

            FOR ALL-DAY EVENTS:
            {{
            "timezone": "IANA_TIMEZONE_ID",
            "assignments": [
                {{
                "summary": "Midterm Exam",
                "start": "2026-03-24",
                "end": "2026-03-24",
                "description": "Chapters 1-5"
                }}
            ]
            }}

            RETURN ONLY A VALID JSON OBJECT.

            SYLLABUS TEXT:
            {markdown_text}
            """

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            raw = response.text.strip().strip("`").replace("json", "").strip()
            data = json.loads(raw)
            if not isinstance(data, dict) or "assignments" not in data:
                raise ValueError("Model did not return expected JSON structure")
            return data
        except json.JSONDecodeError as e:
            last_error = e
            logger.warning("Invalid JSON from model (attempt %s): %s", attempt + 1, e)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_SEC)
        except Exception as e:
            err_str = str(e).lower()
            if "503" in err_str or "unavailable" in err_str or "resource exhausted" in err_str:
                last_error = e
                logger.warning("Transient API error (attempt %s): %s", attempt + 1, e)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY_SEC)
            else:
                raise

    raise ValueError("Model returned invalid JSON after retries") from last_error
