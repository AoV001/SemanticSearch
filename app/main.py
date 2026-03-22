from fastapi import FastAPI
from app.api import upload
from app.api import search


app = FastAPI()
app.include_router(upload.router, prefix="/api")
app.include_router(search.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Semantic Search API running"}