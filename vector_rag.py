from similarity import get_embedding, cosine_similarity
from llm import ask_llm


DOCUMENTS = [
    "Revenue is calculated as quantity multiplied by price.",
    "A high-value product generates more than $1000 in revenue.",
    "The sales report is refreshed every morning at 7 AM."
]


def retrieve(question: str, k: int = 2):
    question_vector = get_embedding(question)

    results = []

    for document in DOCUMENTS:
        document_vector = get_embedding(document)

        score = cosine_similarity(
            question_vector,
            document_vector
        )

        results.append({
            "document": document,
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:k]


async def answer_with_rag(question: str):
    
    retrieved = retrieve(question, k=2)

    context = "\n".join(
        item["document"] for item in retrieved
    )

    prompt = f"""
    Answer the question using ONLY the context below.

    If some parts of the question cannot be answered,
    answer the supported parts and identify what is missing.

    Context:
    {context}

    Question:
    {question}
    """

    answer = await ask_llm(prompt)

    return {
        "question": question,
        "retrieved_documents": retrieved,
        "answer": answer
    }