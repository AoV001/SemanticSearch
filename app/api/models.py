from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    text: str
    question: List[str]
    top_k: int = 3