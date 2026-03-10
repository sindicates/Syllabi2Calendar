from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Placeholder implementation for now
    return JSONResponse({"filename": file.filename, "status": "received"})

