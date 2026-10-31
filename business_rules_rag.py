import chromadb
import httpx


def retrieve_business_rules(question: str) -> list[str]:
    """Retrieve business rules from Chroma."""

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_collection(
        name="business_rules"
    )

    response = httpx.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": question
        },
        timeout=120,
    )

    response.raise_for_status()

    embedding = response.json()["embeddings"][0]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=2,
    )

    return results["documents"][0]
