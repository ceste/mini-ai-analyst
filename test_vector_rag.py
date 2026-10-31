import asyncio

from vector_rag import answer_with_rag


async def main():
    # questions = [
    #     "What qualifies as a high-value product?",
    #     "When is the sales report refreshed?"
    # ]
    questions = [
        "How do we calculate revenue, and what makes a product high-value?"
    ]

    for question in questions:

        result = await answer_with_rag(question)

        print("\nQuestion:", result["question"])
        for item in result["retrieved_documents"]:
            print(
                f"Retrieved ({item['score']:.4f}):",
                item["document"]
            )

    print("Answer:", result["answer"])

asyncio.run(main())