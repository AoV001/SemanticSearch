from fastapi import APIRouter, File, UploadFile
import os

from app.services.file_service import read_txt_file
from app.nlp.text_processing import split_sentences

# api to upload the txt. files

router = APIRouter()

UPLOAD_FOLDER = "data/"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        return {"error": "Only TXT Files are allowed"}

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb+") as f:
        f.write(await file.read())

    text = read_txt_file(file_location)

    sentences = split_sentences(text)

    return {"filename": file.filename, "length": len(text), "sentences": sentences[:5]}