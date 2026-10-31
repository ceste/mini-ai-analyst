from search_documents import search_documents
from llm import ask_llm


async def answer_with_chroma(question: str):

    # 1. Retrieve relevant documents
    results = search_documents(question, k=2)

    documents = results["documents"][0]

    # 2. Combine documents into context
    context = "\n".join(documents)

    # 3. Construct prompt
    # prompt = f"""
    # You are a business analyst.

    # Answer the question using ONLY the context below.
    # If the context does not contain enough information,
    # say what is unavailable.

    # Answer only what the user asks.

    # Context:
    # {context}

    # Question:
    # {question}
    # """

    prompt = f"""
	Answer the question using ONLY the context below.

	If some parts of the question cannot be answered,
	answer the supported parts and identify what is missing.

	Context:
	{context}

	Question:
	{question}
	"""

    # 4. Ask Qwen
    answer = await ask_llm(prompt)

    return {
        "question": question,
        "retrieved_documents": documents,
        "answer": answer
    }