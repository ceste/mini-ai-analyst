import chromadb

from similarity import get_embedding
from chunking import chunk_text
from sentence_chunking import sentence_chunk_text


DOCUMENT = """
Revenue is calculated as quantity multiplied by price.
A high-value product generates more than $1000 in revenue.
The sales report is refreshed every morning at 7 AM.
The company does not track individual customer purchases.
"""


client = chromadb.PersistentClient(path="./chroma_db")


def index_chunks(collection_name, chunks):
    collection = client.get_or_create_collection(
        name=collection_name,
        configuration={"hnsw": {"space": "cosine"}}
    )

    # Reset this experiment's collection
    existing_ids = collection.get()["ids"]

    if existing_ids:
        collection.delete(ids=existing_ids)

    for i, chunk in enumerate(chunks):
        collection.upsert(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            embeddings=[get_embedding(chunk)]
        )

    return collection


def search(collection, question):
    question_vector = get_embedding(question)

    result = collection.query(
        query_embeddings=[question_vector],
        n_results=1
    )

    return (
        result["documents"][0][0],
        result["distances"][0][0]
    )


def main():
    fixed = chunk_text(
        DOCUMENT,
        chunk_size=10,
        overlap=0
    )

    sentence = sentence_chunk_text(
        DOCUMENT,
        max_words=10
    )

    fixed_collection = index_chunks(
        "fixed_chunks", fixed
    )

    sentence_collection = index_chunks(
        "sentence_chunks_test", sentence
    )

    questions = [
        "What makes a product high-value?",
        "When is the sales report refreshed?",
        "Does the company track individual purchases?"
    ]

    for question in questions:
        fixed_doc, fixed_distance = search(
            fixed_collection, question
        )

        sentence_doc, sentence_distance = search(
            sentence_collection, question
        )

        print(f"\nQuestion: {question}")

        print(
            f"Fixed ({fixed_distance:.4f}):",
            fixed_doc
        )

        print(
            f"Sentence ({sentence_distance:.4f}):",
            sentence_doc
        )


if __name__ == "__main__":
    main()