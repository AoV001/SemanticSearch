from fastapi import APIRouter
from app.api.models import SearchRequest
from app.services.search_service import search
from app.nlp.answer_extraction import format_triplets

router = APIRouter()

@router.post("/search")
def search_endpoint(request: SearchRequest):
    all_results = search(
        questions=request.questions,
        text=request.text,
        top_k=request.top_k,
    )

    response = []

    for question, results in all_results.items():
        question_data = {
            "question": question,
            "results": []
        }

        for block, score, triplets, answer in results:
            question_data["results"].append({
                "answer": answer or "—",
                "confidence": round(score, 2),
                "context": block,
                "evidence": format_triplets(triplets)
            })

        response.append(question_data)

    return response