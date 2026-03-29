from fastapi import APIRouter
from app.db.history import get_history, clear_history, get_history_by_file
"""
Search History API Router

This module defines FastAPI endpoints for managing search history
within the application.

Endpoints:
    GET /history
        Returns the most recent search history entries.
        Optional query parameter:
            - limit (int): Maximum number of records to return (default: 50).

    GET /history/{filename}
        Returns search history entries related to a specific file.

    DELETE /history
        Clears all stored search history entries.

Dependencies:
    app.db.history.get_history
        Retrieves the latest history records.

    app.db.history.get_history_by_file
        Retrieves history entries associated with a specific file.

    app.db.history.clear_history
        Removes all stored history records.
"""

router = APIRouter()

@router.get("/history")
def get_search_history(limit: int = 50):
    return {"history": get_history(limit)}

@router.get("/history/{filename}")
def get_file_history(filename: str):
    return {"history": get_history_by_file(filename)}

@router.delete("/history")
def clear_search_history():
    clear_history()
    return {"message": "History cleared"}