from fastapi import APIRouter, File, UploadFile, HTTPException
import os
from pydantic import BaseModel
from app.services.file_service import (
    read_file, ensure_upload_folder,
    list_files, delete_file, file_exists, delete_all_files
)
from app.nlp.text_processing import split_sentences
"""
File Management API Router

Provides endpoints for uploading, reading, listing, and deleting text or PDF files
used by the search system.

Main features:
- Upload files (.txt, .pdf) with size validation
- Upload raw text as a file
- List available files
- Retrieve full text of a file
- Delete a specific file or all files

Limits:
- Maximum file size: 5 MB
- Maximum text length (text upload): 5000 characters
- Maximum filename length: 100 characters
"""

router = APIRouter()
UPLOAD_FOLDER = "data/"
ALLOWED_EXTENSIONS = {".txt", ".pdf"}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_TEXT_LENGTH = 5000
MAX_FILENAME_LENGTH = 100

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are allowed")

    ensure_upload_folder()

    if file_exists(file.filename):
        raise HTTPException(status_code=409, detail=f"File '{file.filename}' already exists")

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 5MB")

    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(content)

    text = read_file(file_location)
    sentences = split_sentences(text)

    return {
        "filename": file.filename,
        "format": ext.lstrip("."),
        "length": len(text),
        "sentences_total": len(sentences),
        "preview": sentences[:5]
    }

@router.get("/files")
def get_files():
    files = list_files()
    return {"files": files, "total": len(files)}

@router.get("/files/{filename}/text")
def get_file_text(filename: str):
    if not file_exists(filename):
        raise HTTPException(status_code=404, detail="File not found")
    text = read_file(os.path.join(UPLOAD_FOLDER, filename))
    return {"text": text}

@router.delete("/files/{filename}")
def delete_file_endpoint(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are allowed")

    if not file_exists(filename):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    delete_file(filename)
    return {"message": f"File '{filename}' deleted successfully"}

@router.delete("/files")
def delete_all_files_endpoint():
    count = delete_all_files()
    return {"message": f"Deleted {count} files"}

class TextInput(BaseModel):
    text: str
    filename: str


@router.post("/upload-text")
def upload_text(data: TextInput):
    if not data.filename.strip():
        raise HTTPException(status_code=400, detail="Filename cannot be empty")

    if len(data.text) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=413, detail=f"Text too long. Maximum is {MAX_TEXT_LENGTH} characters")

    filename = data.filename if data.filename.endswith(".txt") else data.filename + ".txt"

    if len(filename) > MAX_FILENAME_LENGTH:
        raise HTTPException(status_code=400, detail="Filename too long")

    if file_exists(filename):
        raise HTTPException(status_code=409, detail=f"File '{filename}' already exists")

    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    ensure_upload_folder()
    file_location = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_location, "w", encoding="utf-8") as f:
        f.write(data.text)

    sentences = split_sentences(data.text)

    return {
        "filename": filename,
        "format": "txt",
        "length": len(data.text),
        "sentences_total": len(sentences),
        "preview": sentences[:5]
    }