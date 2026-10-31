import os
import httpx


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5:7b"
)

async def ask_llm(question: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": question,
                    "stream": False
                },
                timeout=30.0
            )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except httpx.RequestError as e:
        raise RuntimeError(
            f"LLM service unavailable: {e}"
        )

# def ask_llm(question: str):
#     try:
#         response = httpx.post(
#             OLLAMA_URL,
#             json={
#                 "model": MODEL,
#                 "prompt": question,
#                 "stream": False
#             },
#             timeout=30.0
#         )

#         response.raise_for_status()

#         data = response.json()

#         return data["response"]

#     except httpx.RequestError as e:
#         raise RuntimeError(
#             f"LLM service unavailable: {e}"
#         )


# async def choose_action(question: str):
#     prompt = f"""
#             You are a router.

#             Available actions:

#             DIRECT
#             Use this when the question can be answered without company sales data.

#             GET_PRODUCT_REVENUE
#             Use this when the question requires product revenue or sales data.

#             User question:
#             {question}

#             Return ONLY one of these:
#             DIRECT
#             GET_PRODUCT_REVENUE
#             """

#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 OLLAMA_URL,
#                 json={
#                     "model": MODEL,
#                     "prompt": prompt,
#                     "stream": False
#                 },
#                 timeout=30.0
#             )

#         response.raise_for_status()

#         return response.json()["response"].strip()

#     except httpx.RequestError as e:
#         raise RuntimeError(
#             f"LLM service unavailable: {e}"
#         )

async def choose_action(question: str):

    prompt = f"""
                You are a router for an AI analyst.

                Available actions:

                DIRECT
                Use ONLY when the question does not require company sales data.

                GET_PRODUCT_REVENUE
                Use when the user asks about:
                - a specific product's revenue
                - revenue by product
                - comparing products
                - which product has highest/lowest revenue

                Optional argument:
                product = product name when a specific product is requested.

                GET_TOTAL_REVENUE
                Use when the user asks about:
                - total revenue
                - overall revenue
                - combined revenue
                - whether total revenue is above or below an amount

                Important:
                If the question is about TOTAL revenue, choose GET_TOTAL_REVENUE,
                not GET_PRODUCT_REVENUE.

                User question:
                {question}

                Return ONLY valid JSON using exactly this structure:

                {{
                    "action": "DIRECT or GET_PRODUCT_REVENUE",
                    "arguments": {{}}
                }}

                Do not include markdown.
                Do not include explanation.
                """

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0
                    }
                },
                timeout=30.0
            )

        response.raise_for_status()

        return response.json()["response"]

    except httpx.RequestError as e:
        raise RuntimeError(
            f"LLM service unavailable: {e}"
        )