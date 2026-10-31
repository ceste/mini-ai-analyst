import chromadb

from similarity import get_embedding


# Open our existing vector database
client = chromadb.PersistentClient(path="./chroma_db")

# Access the collection created earlier
collection = client.get_collection(
    name="business_rules"
)


def search_documents(question: str, k: int = 2):

    # Only the question needs a new embedding
    question_embedding = get_embedding(question)

    # Search the saved document vectors
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=k
    )

    return results


if __name__ == "__main__":

    question = (
        "How do we calculate revenue, "
        "and what makes a product high-value?"
    )

    results = search_documents(question)

    # print(results)

    print("Question:", question)

    for document, distance in zip(
        results["documents"][0],
        results["distances"][0]
    ):
        print("\nRetrieved:", document)
        print("Distance:", round(distance, 4))