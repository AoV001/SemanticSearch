from fastapi import APIRouter, File, UploadFile
import os

router = APIRouter()
UPLOAD_FOLDER = "data/"
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb+") as f:
        f.write(await file.read())
    return {"filename": file.filename}