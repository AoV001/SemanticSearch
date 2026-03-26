from fastapi import APIRouter
from app.db.history import get_history, clear_history

router = APIRouter()

@router.get("/history")
def get_search_history(limit: int = 50):
    return {"history": get_history(limit)}

@router.delete("/history")
def clear_search_history():
    clear_history()
    return {"message": "History cleared"}