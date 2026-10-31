
import json
import httpx

from tool_registry import execute_tool


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"


def choose_tool(question: str) -> dict:
    prompt = f"""
                You are a tool-selection assistant.

                Available tool:
                - classify_products: Classify products as high-value
                  based on their revenue.

                Return ONLY valid JSON in this format:
                {{
                    "tool": "classify_products",
                    "arguments": {{
                        "products": [
                            {{"product": "Laptop", "revenue": 2400}},
                            {{"product": "Monitor", "revenue": 900}}
                        ]
                    }}
                }}

                Use only the product data provided in the question.
                Never invent product names or revenue figures.
                If the question cannot be answered using the available
                tool and provided data, return:
                {{"tool": "none", "arguments": {{}}}}

                Question: {question}
                """

    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=120
    )

    response.raise_for_status()

    content = response.json()["message"]["content"]
    return json.loads(content)


def main():
    question = (
        "Classify these products: "
        "Laptop revenue is 2400, "
        "Monitor revenue is 900."
    )

    decision = choose_tool(question)
    print("Qwen decision:", decision)

    tool_name = decision["tool"]

    if tool_name == "none":
        print("No suitable tool available.")
        return

    result = execute_tool(
        tool_name,
        decision["arguments"]
    )

    print("Tool result:", result)


if __name__ == "__main__":
    main()
