from fastapi import APIRouter
from app.api.models import SearchRequest
from app.services.search_service import search

router = APIRouter()

@router.post("/search")
def search_endpoint(request: SearchRequest):

    results = search(
        question = request.question,
        text = request.text,
        top_k = request.top_k,
    )

    response = []

    for sentence, score in results:
        response.append({
            "sentence": sentence,
            "score": score
        })
    return response