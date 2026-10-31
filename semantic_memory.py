import chromadb
# import requests

# from conversation_memory import load_fact
from app.memory.conversation_memory import load_fact


# Reuse the embedding approach from Lesson 4
# def embed(text):

#     response = requests.post(
#         "http://localhost:11434/api/embed",
#         json={
#             "model": "nomic-embed-text",
#             "input": text
#         },
#         timeout=60
#     )

#     response.raise_for_status()

#     return response.json()["embeddings"][0]

from app.embeddings.ollama_embeddings import embed

client = chromadb.PersistentClient(
    path="./memory_chroma_db"
)

collection = client.get_or_create_collection(
    name="long_term_memories"
)


def initialize_semantic_memory():

    keys = [
        "high_value_threshold",
        "revenue_formula"
    ]

    descriptions = [
        "The minimum revenue required for a product "
        "to qualify as a high-value product. "
        "The high-value revenue threshold.",

        "How product revenue is calculated. "
        "The formula for calculating revenue "
        "using quantity and price."
    ]

    embeddings = [
        embed(description)
        for description in descriptions
    ]

    collection.upsert(
        ids=keys,
        documents=descriptions,
        embeddings=embeddings
    )


# def search_memory(question):

#     question_embedding = embed(question)

#     results = collection.query(
#         query_embeddings=[question_embedding],
#         n_results=1
#     )

#     if not results["ids"][0]:
#         return None

#     memory_key = results["ids"][0][0]

#     return {
#         "key": memory_key,
#         "value": load_fact(memory_key),
#         "distance": results["distances"][0][0]
#     }


def search_memory(question, max_distance=0.6):

    question_embedding = embed(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1
    )

    if not results["ids"][0]:
        return None

    memory_key = results["ids"][0][0]
    distance = results["distances"][0][0]

    # Reject memories that are too far from the question.
    if distance > max_distance:
        return None

    return {
        "key": memory_key,
        "value": load_fact(memory_key),
        "distance": distance
    }
