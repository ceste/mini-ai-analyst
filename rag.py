from pathlib import Path
from llm import ask_llm

DOCUMENT_PATH = Path(__file__).parent / "docs" / "business_rules.txt"


def retrieve_context():
    return DOCUMENT_PATH.read_text(encoding="utf-8")

async def answer_from_document(question: str):
    
    context = retrieve_context()

    prompt = f"""
    You are a business analyst.

    Answer the question using ONLY the context below.

    If the context does not contain enough information,
    say that the information is unavailable.

    Context:
    {context}

    Question:
    {question}
    """

    return await ask_llm(prompt)
