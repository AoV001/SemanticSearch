import os
import pdfplumber
from app.db.history import delete_history_by_file

"""
File Service Utilities

Provides functions for reading, managing, and maintaining uploaded files
and their associated search history.

Key Features:
- read_file(path): reads text from .txt or .pdf files
- ensure_upload_folder(): creates the upload folder if missing
- list_files(): lists all .txt and .pdf files in the upload folder
- delete_file(filename): deletes a file and clears its search history
- file_exists(filename): checks if a file exists
- delete_all_files(): deletes all uploaded files and returns the count
"""

UPLOAD_FOLDER = "data/"


def read_txt_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf_file(path: str) -> str:
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def read_file(path: str) -> str:
    if path.endswith(".pdf"):
        return read_pdf_file(path)
    return read_txt_file(path)


def ensure_upload_folder():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def list_files() -> list[str]:
    ensure_upload_folder()
    return [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".txt", ".pdf"))]


def delete_file(filename: str) -> bool:
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return False
    os.remove(path)
    delete_history_by_file(filename)
    return True


def file_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(UPLOAD_FOLDER, filename))


def delete_all_files() -> int:
    ensure_upload_folder()
    files = list_files()
    for f in files:
        delete_file(f)
    return len(files)
