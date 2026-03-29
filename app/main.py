from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, search, history
from app.db.database import init_db

"""
Main FastAPI app

- Initializes database
- Configures CORS for frontend at http://localhost:5173
- Registers API routers:
    - /api/upload   : file and text upload endpoints
    - /api/search   : semantic search endpoints
    - /api/history  : search history endpoints
- Root endpoint (/) returns a simple status message
"""

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(history.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Semantic Search API running"}