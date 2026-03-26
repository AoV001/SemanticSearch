from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, search, history
from app.db.database import init_db


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