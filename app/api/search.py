from fastapi import APIRouter, HTTPException
from app.api.models import SearchRequest
from app.services.search_service import search
from app.nlp.answer_extraction import format_triplets
from app.services.file_service import read_file, file_exists
import os

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

    results_data, resolved_text = all_results
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
                "evidence": format_triplets(triplets)
            })

        response.append(question_data)

    return {"results": response, "resolved_text": resolved_text}