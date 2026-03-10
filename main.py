# Import Libraries
import pymupdf4llm
import fitz
from fastapi import FastAPI, UploadFile, File
import os
from dotenv import load_dotenv
from services.ai_service import extract_assignments
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

    return {
        "filename": file.filename,
        "raw_markdown": md_text,
        "assignments": assignments,
    }
