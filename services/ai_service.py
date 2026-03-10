from google import genai
from google.genai import types
import os
import json
import json as _json
from pathlib import Path
import time as _time

from dotenv import load_dotenv

load_dotenv(".env.local")

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def extract_assignments(markdown_text):
    model_name = "gemini-3.1-flash-lite-preview"

    prompt = f"""
            You are an academic data engineer. Extract all assignments, quizzes, and exams from the syllabus.
            Return ONLY a JSON array.

            TIMEZONE & LOCALIZATION RULES:
            1. SCHOOL IDENTIFICATION: Identify the school/university from the syllabus text.
            2. TIMEZONE DETECTION: Determine the exact IANA Timezone ID for that school (e.g., 'America/New_York' for CWRU, 'America/Chicago' for UChicago).
            3. TIMED EVENTS: If a specific clock time is mentioned (e.g., 2:00 PM), return it in "YYYY-MM-DDTHH:MM:SS" format. 
            Do NOT include a UTC offset (like +00:00).
            4. ALL-DAY EVENTS: If NO time is mentioned, return ONLY "YYYY-MM-DD".
            5. DURATION: If an end time is missing, set it to 1 hour after the start time.
            6. ASSIGNMENT DUE DATES: If a syllabus says "Due by [Date]" with no time, return ONLY the date (All-Day).

            JSON STRUCTURE:
            {{
            "timezone": "IANA_TIMEZONE_ID", 
            "assignments": [
                {{
                "summary": "Midterm Exam",
                "start": "2026-03-24T14:00:00",
                "end": "2026-03-24T15:00:00",
                "description": "Chapters 1-5"
                }}
            ]
            }}

            SYLLABUS TEXT:
            {markdown_text}
            """
  
    response = client.models.generate_content(model=model_name, contents=prompt)

    return json.loads(response.text.strip("`").replace("json", ""))