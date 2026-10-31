import chromadb

from similarity import get_embedding


DOCUMENTS = [
    "Revenue is calculated as quantity multiplied by price.",
    "A high-value product generates more than $1000 in revenue.",
    "The sales report is refreshed every morning at 7 AM."
]


# Create a persistent local database
client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection, or open it if it already exists
collection = client.get_or_create_collection(
    name="business_rules",
    configuration={"hnsw": {"space": "cosine"}}
)


def main():
	
    for index, document in enumerate(DOCUMENTS):

        embedding = get_embedding(document)

        collection.upsert(
            ids=[f"rule_{index}"],
            documents=[document],
            embeddings=[embedding]
        )

        print(f"Stored: {document}")

    print("\nTotal documents:", collection.count())


if __name__ == "__main__":
    main()