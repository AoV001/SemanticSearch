from pydantic import BaseModel, field_validator
from typing import List

MAX_QUESTION_LENGTH = 200
MAX_QUESTIONS_COUNT = 20

class SearchRequest(BaseModel):
    filename: str
    questions: List[str]
    top_k: int = 3

    @field_validator("questions")
    @classmethod
    def validate_questions(cls, v):
        if not v:
            raise ValueError("questions list cannot be empty")
        if len(v) > MAX_QUESTIONS_COUNT:
            raise ValueError(f"Too many questions. Maximum is {MAX_QUESTIONS_COUNT}")
        for q in v:
            if not q.strip():
                raise ValueError("questions cannot contain empty strings")
            if len(q) > MAX_QUESTION_LENGTH:
                raise ValueError(f"Question too long. Maximum is {MAX_QUESTION_LENGTH} characters")
        return v