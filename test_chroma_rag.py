import asyncio

from chroma_rag import answer_with_chroma


async def main():

    question = (
        "How do we calculate revenue, "
        "and what makes a product high-value?"
    )

    result = await answer_with_chroma(question)

    print("\nQuestion:", result["question"])

    print("\nRetrieved documents:")
    for document in result["retrieved_documents"]:
        print("-", document)

    print("\nAnswer:", result["answer"])


if __name__ == "__main__":
    asyncio.run(main())