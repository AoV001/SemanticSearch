from fastapi import FastAPI
from app.api import upload
from app.api import search
from app.db.database import init_db
from app.api import history


app = FastAPI()
init_db()
app.include_router(upload.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(history.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Semantic Search API running"}