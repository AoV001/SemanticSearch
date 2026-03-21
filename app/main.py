from fastapi import FastAPI
from app.api import upload

app = FastAPI()
app.include_router(upload.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Semantic Search API running"}