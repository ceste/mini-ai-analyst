from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import HTTPException
import time
import asyncio

from database import get_connection, initialize_database
# from llm import ask_llm
from service import answer_question

app = FastAPI()

initialize_database()

@app.get("/")
def home():
    return {"message": "Mini AI Analyst is running"}


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    return {
        "customer_id": customer_id,
        "segment": "high_value"
    }


class Question(BaseModel):
    question: str

# @app.post("/ask")
# def ask(question: Question):
#     return {
#         "received_question": question.question,
#         "answer": "Not intelligent yet!"
#     }

# @app.post("/ask")
# def ask(question: Question):

#     answer = ask_llm(question.question)

#     return {
#         "question": question.question,
#         "answer": answer
#     }

# @app.post("/ask")
# def ask(question: Question):
#     try:
#         answer = ask_llm(question.question)

#         return {
#             "question": question.question,
#             "answer": answer
#         }

#     except RuntimeError:
#         raise HTTPException(
#             status_code=503,
#             detail="AI service temporarily unavailable"
#         )

# @app.post("/ask")
# async def ask(question: Question):
#     try:
#         answer = await ask_llm(question.question)

#         return {
#             "question": question.question,
#             "answer": answer
#         }

#     except RuntimeError:
#         raise HTTPException(
#             status_code=503,
#             detail="AI service temporarily unavailable"
#         )


@app.post("/ask")
async def ask(question: Question):
    try:
        answer = await answer_question(question.question)

        return {
            "question": question.question,
            "answer": answer
        }

    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable"
        )
        
@app.get("/sales")
def get_sales():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product, quantity, price
        FROM sales
    """)

    rows = cursor.fetchall()
    conn.close()

    return {
        "sales": [
            {
                "product": row[0],
                "quantity": row[1],
                "price": row[2]
            }
            for row in rows
        ]
    }    


@app.get("/slow")
def slow():
    time.sleep(5)

    return {"message": "finished"}

@app.get("/slow-async")
async def slow_async():
    await asyncio.sleep(5)

    return {"message": "finished"}
