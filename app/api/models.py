from pydantic import BaseModel

class SearchRequest(BaseModel):
    text: str
    question: str
    top_k: int = 3