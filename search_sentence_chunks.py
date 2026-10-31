import chromadb

from similarity import get_embedding


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="sentence_rules"
)


def search(question: str, k: int = 2):
    question_embedding = get_embedding(question)

    return collection.query(
        query_embeddings=[question_embedding],
        n_results=k
    )


if __name__ == "__main__":
    question = (
        "When is the sales report refreshed?"
    )

    results = search(question, k=2)

    print("Question:", question)

    for document, distance in zip(
        results["documents"][0],
        results["distances"][0]
    ):
        print("\nRetrieved:", document)
        print("Distance:", round(distance, 4))