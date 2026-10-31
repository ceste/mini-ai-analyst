import chromadb

from similarity import get_embedding


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="sentence_chunks_test"
)


TEST_CASES = [
    {
        "question": "How do we calculate revenue?",
        "expected_id": "chunk_0"
    },
    {
        "question": "What makes a product high-value?",
        "expected_id": "chunk_1"
    },
    {
        "question": "When is the sales report refreshed?",
        "expected_id": "chunk_2"
    },
    {
        "question": "Does the company track individual purchases?",
        "expected_id": "chunk_3"
    }
]


def evaluate():

    hits_at_1 = 0
    hits_at_2 = 0

    for test in TEST_CASES:

        question_vector = get_embedding(
            test["question"]
        )

        results = collection.query(
            query_embeddings=[question_vector],
            n_results=2
        )

        retrieved_ids = results["ids"][0]
        expected_id = test["expected_id"]

        hit_1 = expected_id == retrieved_ids[0]
        hit_2 = expected_id in retrieved_ids[:2]

        hits_at_1 += int(hit_1)
        hits_at_2 += int(hit_2)

        print("\nQuestion:", test["question"])
        print("Expected:", expected_id)
        print("Retrieved:", retrieved_ids)
        print("Hit@1:", hit_1)
        print("Recall@2:", hit_2)

    total = len(TEST_CASES)

    print("\n--- Evaluation Summary ---")
    print(f"Hit@1: {hits_at_1}/{total} = {hits_at_1 / total:.1%}")
    print(f"Recall@2: {hits_at_2}/{total} = {hits_at_2 / total:.1%}")


if __name__ == "__main__":
    evaluate()