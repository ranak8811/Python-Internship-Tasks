from fastapi import FastAPI
from pydantic import BaseModel
from rag import answer_question

app = FastAPI(title="Samsung Phone Advisor")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    answer = answer_question(req.question)
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"message": "Samsung Phone Advisor API is running"}
