from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import answer_question

app = FastAPI(title="Samsung Phone Advisor")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    # answer = answer_question(req.question)
    # return {"answer": answer}
    try:
        answer = answer_question(req.question)

        if not isinstance(answer, str):
            raise ValueError("Invalid answer format")

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

@app.get("/")
def read_root():
    return {"message": "Samsung Phone Advisor API is running"}
