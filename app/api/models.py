from pydantic import BaseModel, field_validator
from typing import List

"""
Search Request Schema

This module defines the data model used for search requests in the API.
It uses Pydantic for request validation and data parsing.

The SearchRequest model represents a client request that performs a
semantic search over a specific file using one or multiple questions.

Fields:
    filename (str)
        Name of the file in which the search will be performed.

    questions (List[str])
        A list of user questions or queries used for the search.
        The list must not be empty and must not exceed MAX_QUESTIONS_COUNT.

    top_k (int)
        Number of most relevant results to return for each question.
        Default value is 3.

Validation Rules:
    - The questions list must not be empty.
    - The number of questions must not exceed MAX_QUESTIONS_COUNT.
    - Each question must not be an empty string.
    - Each question must not exceed MAX_QUESTION_LENGTH characters.

Constants:
    MAX_QUESTION_LENGTH
        Maximum allowed length of a single question.

    MAX_QUESTIONS_COUNT
        Maximum number of questions allowed in a request.
"""

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
                raise ValueError(
                    f"Question too long. Maximum is {MAX_QUESTION_LENGTH} characters"
                )
        return v
