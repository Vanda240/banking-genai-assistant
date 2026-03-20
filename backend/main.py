from fastapi import FastAPI
from pydantic import BaseModel
from src.rag_answer import generate_answer

app = FastAPI()


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask_question(request: AskRequest):
    answer, sources = generate_answer(request.question)
    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }