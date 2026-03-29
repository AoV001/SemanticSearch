from fastapi import APIRouter, HTTPException
from app.api.models import SearchRequest
from app.services.search_service import search
from app.nlp.answer_extraction import format_triplets
from app.services.file_service import read_file, file_exists
import os
"""
Search API Router

This module defines the FastAPI endpoint responsible for performing
semantic search over uploaded or stored text files.

The endpoint accepts a SearchRequest containing a filename and a list
of questions. It retrieves the file content, runs the search pipeline,
and returns ranked results for each question.

Endpoint:
    POST /search
        Executes a semantic search over the specified file.

Workflow:
    1. Validate that the requested file exists.
    2. Read the file content from the data directory.
    3. Pass the questions and text to the search service.
    4. Process the returned results and format them for the API response.

Response Structure:
    results
        A list of question-specific search results containing:
            - question: the original query
            - results: list of matching text blocks with:
                - answer: extracted answer (if available)
                - confidence: similarity score
                - context: text fragment where the match was found
                - evidence: formatted triplets used as evidence
                - triplets: structured subject–relation–object data

    resolved_text
        The processed text after coreference resolution.

    coref_map
        A mapping of resolved coreferences used during text processing.

Dependencies:
    app.api.models.SearchRequest
        Request schema defining input validation.

    app.services.search_service.search
        Main search pipeline that retrieves relevant text fragments.

    app.services.file_service.read_file
        Reads file content from the data directory.

    app.services.file_service.file_exists
        Checks whether the requested file exists.

    app.nlp.answer_extraction.format_triplets
        Formats extracted knowledge triplets for API output.

Error Handling:
    Returns HTTP 404 if the requested file does not exist.
"""

router = APIRouter()

@router.post("/search")
def search_endpoint(request: SearchRequest):
    if not file_exists(request.filename):
        raise HTTPException(
            status_code=404,
            detail=f"File '{request.filename}' not found")

    text = read_file(os.path.join("data/", request.filename))
    all_results = search(
        questions=request.questions,
        text=text,
        top_k=request.top_k,
        filename=request.filename)

    results_data, resolved_text, coref_map = all_results
    response = []

    for question, hits in results_data.items():
        question_data = {
            "question": question,
            "results": []
        }

        for block, score, triplets, answer in hits:
            question_data["results"].append({
                "answer": answer or "—",
                "confidence": round(score, 2),
                "context": block,
                "evidence": format_triplets(triplets),
                "triplets": [{"from": u, "rel": rel, "to": v} for u, rel, v in triplets]
            })

        response.append(question_data)

    return {"results": response, "resolved_text": resolved_text, "coref_map": coref_map}