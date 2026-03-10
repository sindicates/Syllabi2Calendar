# Import Libraries
import pymupdf4llm
import fitz
from fastapi import FastAPI, UploadFile, File
import os
from dotenv import load_dotenv
from services.ai_service import extract_assignments
from services.calendar_service import create_event, get_calendar_service

import json as _json
import time as _time

# Initialize FastAPI
app = FastAPI()
load_dotenv()

# Home Route
@app.get("/")
def home():
    return {"message": "Scanner Backend is Online"}


# Scan PDF Route
@app.post("/scan")


async def scan_pdf(file: UploadFile = File(...)):
    
    content = await file.read()

    doc = fitz.open(stream=content, filetype="pdf")

    md_text = pymupdf4llm.to_markdown(doc=doc)

    assignments = extract_assignments(markdown_text=md_text)

    school_tz = assignments.get("timezone")
    events_to_create = assignments.get("assignments", [])

    created_event_links = []

    # region agent log
    try:
        with open("debug-b18514.log", "a", encoding="utf-8") as _f:
            _f.write(_json.dumps({
                "sessionId": "b18514",
                "runId": "pre-fix",
                "hypothesisId": "H1",
                "location": "main.py:scan_pdf",
                "message": "Assignments extracted",
                "data": {
                    "has_timezone": school_tz is not None,
                    "timezone": school_tz,
                    "events_count": len(events_to_create)
                },
                "timestamp": int(_time.time() * 1000)
            }) + "\n")
    except Exception:
        pass
    # endregion agent log

    for item in events_to_create: 
        
        try: 
            link = create_event(event_data=item, school_tz=school_tz)

            # region agent log
            try:
                with open("debug-b18514.log", "a", encoding="utf-8") as _f:
                    _f.write(_json.dumps({
                        "sessionId": "b18514",
                        "runId": "pre-fix",
                        "hypothesisId": "H2",
                        "location": "main.py:scan_pdf",
                        "message": "create_event result",
                        "data": {
                            "event_summary": item.get("summary"),
                            "link_is_none": link is None
                        },
                        "timestamp": int(_time.time() * 1000)
                    }) + "\n")
            except Exception:
                pass
            # endregion agent log

            if link:
                created_event_links.append(link)

        except Exception as e:
            print(f"Error creating event: {e}")

            # region agent log
            try:
                with open("debug-b18514.log", "a", encoding="utf-8") as _f:
                    _f.write(_json.dumps({
                        "sessionId": "b18514",
                        "runId": "pre-fix",
                        "hypothesisId": "H3",
                        "location": "main.py:scan_pdf",
                        "message": "Error in create_event",
                        "data": {
                            "event_summary": item.get("summary"),
                            "error": str(e)
                        },
                        "timestamp": int(_time.time() * 1000)
                    }) + "\n")
            except Exception:
                pass
            # endregion agent log

            continue

    return {
        "events_created": len(created_event_links),
        "links": created_event_links
    }
