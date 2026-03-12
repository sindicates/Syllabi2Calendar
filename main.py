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

    return assignments
    created_event_links = []

    for event in events_to_create:
        
        try:

            event_link = create_event(event_data=event, school_tz=school_tz)
            created_event_links.append(event_link)

        except Exception as e:
            print(f"Error creating event: {e}")
            continue

    return {
        "events_created": len(created_event_links),
        "links": created_event_links
    }
