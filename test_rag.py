import asyncio

from rag import answer_from_document


async def main():
    questions = [
        "What makes a product high-value?",
        "When is the sales report refreshed?",
        "How many customers bought Laptop?"
    ]

    for question in questions:
        answer = await answer_from_document(question)

        print(f"\nQuestion: {question}")
        print(f"Answer: {answer}")


asyncio.run(main())