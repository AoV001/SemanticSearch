# return the whole txt.- file as a single string
def read_txt_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()