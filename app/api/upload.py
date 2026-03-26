from fastapi import APIRouter, File, UploadFile, HTTPException
import os

from app.services.file_service import (
    read_txt_file, ensure_upload_folder,
    list_files, delete_file, file_exists
)
from app.nlp.text_processing import split_sentences

router = APIRouter()
UPLOAD_FOLDER = "data/"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    ensure_upload_folder()

    if file_exists(file.filename):
        raise HTTPException(status_code=409, detail=f"File '{file.filename}' already exists")

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    content = await file.read()
    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    with open(file_location, "wb") as f:
        f.write(content)

    text = read_txt_file(file_location)
    sentences = split_sentences(text)

    return {
        "filename": file.filename,
        "length": len(text),
        "sentences_total": len(sentences),
        "preview": sentences[:5]
    }

@router.get("/files")
def get_files():
    files = list_files()
    return {"files": files, "total": len(files)}

@router.delete("/files/{filename}")
def delete_file_endpoint(filename: str):
    if not filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    if not file_exists(filename):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    delete_file(filename)
    return {"message": f"File '{filename}' deleted successfully"}