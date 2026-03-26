from pydantic import BaseModel, field_validator
from typing import List

class SearchRequest(BaseModel):
    filename: str
    questions: List[str]
    top_k: int = 3

    @field_validator("questions")
    @classmethod
    def questions_not_empty(cls, v):
        if not v:
            raise ValueError("questions list cannot be empty")
        if any(not q.strip() for q in v):
            raise ValueError("questions cannot contain empty strings")
        return v