import os

UPLOAD_FOLDER = "data/"

def read_txt_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_upload_folder():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def list_files() -> list[str]:
    ensure_upload_folder()
    return [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".txt")]

def delete_file(filename: str) -> bool:
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return False
    os.remove(path)
    return True

def file_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(UPLOAD_FOLDER, filename))