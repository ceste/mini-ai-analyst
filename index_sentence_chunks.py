import chromadb

from similarity import get_embedding
from sentence_chunking import sentence_chunk_text


DOCUMENT = """
Revenue is calculated as quantity multiplied by price.
A high-value product generates more than $1000 in revenue.
The sales report is refreshed every morning at 7 AM.
The company does not track individual customer purchases.
"""


def main():
    
    chunks = sentence_chunk_text(
        DOCUMENT,
        max_words=10
    )

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="sentence_rules",
        configuration={"hnsw": {"space": "cosine"}}
    )

    for index, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        collection.upsert(
            ids=[f"sentence_{index}"],
            documents=[chunk],
            embeddings=[embedding]
        )

        print(f"Stored chunk {index + 1}: {chunk}")

    print("\nTotal chunks:", collection.count())


if __name__ == "__main__":
    main()