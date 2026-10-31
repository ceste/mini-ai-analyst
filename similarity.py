import httpx
import math

OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"


def get_embedding(text):
    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "input": text
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()["embeddings"][0]


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    return dot_product / (norm_a * norm_b)

def main():
    
    question = "What qualifies as a high-value product?"

    documents = [
        "Revenue is calculated as quantity multiplied by price.",
        "A high-value product generates more than $1000 in revenue.",
        "The sales report is refreshed every morning at 7 AM."
    ]

    question_vector = get_embedding(question)

    results = []

    for document in documents:
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

    top_document = results[0]

    print("Question:", question)
    print("Retrieved document:", top_document["document"])
    print("Similarity:", round(top_document["score"], 4))



if __name__ == "__main__":
    main()