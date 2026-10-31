import os
os.environ["PYDANTIC_AI_NO_BANNER"] = "1"

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from database import get_connection

from business_rules_rag import retrieve_business_rules
from business_config import HIGH_VALUE_THRESHOLD
from rule_validator import validate_high_value_rule

# HIGH_VALUE_THRESHOLD = 1000

model = OllamaModel(
    "qwen2.5:7b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)

agent = Agent(
    model,
    # instructions=(
    #     "You are a business analytics assistant. "
    #     "For high-value product questions, use "
    #     "get_high_value_products. "
    #     "Use the tool's classification results. "
    #     "Do not recalculate or invent revenue figures."
    # ),
    instructions=(
        "You are a business analytics assistant. "
        "For high-value product questions, use get_high_value_products. "
        "If the tool returns SUCCESS, explain the verified results. "
        "If the tool returns BLOCKED, explain that the business rules "
        "are inconsistent or could not be verified. "
        "Never present a blocked classification as valid. "
        "Do not invent product revenue or business rules."
    ),
)

def get_high_value_analysis() -> dict:
    """Retrieve revenue and classify products in Python."""

    conn = get_connection()

    try:
        rows = conn.execute("""
            SELECT
                product,
                SUM(quantity * price) AS revenue
            FROM sales
            GROUP BY product
        """).fetchall()
    finally:
        conn.close()

    products = [
        {
            "product": product,
            "revenue": revenue,
            "is_high_value": revenue > HIGH_VALUE_THRESHOLD
        }
        for product, revenue in rows
    ]

    return {
        "threshold": HIGH_VALUE_THRESHOLD,
        "operator": ">",
        "products": products
    }


def validate_current_business_rule() -> dict:
    """Validate Chroma's high-value rule before classification."""

    documents = retrieve_business_rules(
        "What is the definition of a high-value product?"
    )

    matching_rules = [
        document
        for document in documents
        if "high-value product" in document.lower()
    ]

    if len(matching_rules) != 1:
        return {
            "status": "UNKNOWN",
            "reason": "Expected exactly one high-value rule."
        }

    return validate_high_value_rule(matching_rules[0])


# @agent.tool_plain
# def get_high_value_products() -> dict:
#     """Retrieve and classify products using Python."""

#     print("High-value workflow executed!")

#     return get_high_value_analysis()


@agent.tool_plain
def get_high_value_products() -> dict:
    """Validate business rules and retrieve classified products."""

    print("Validating business rules...")

    validation = validate_current_business_rule()

    print("Validation result:", validation)

    if validation["status"] != "MATCH":
        return {
            "status": "BLOCKED",
            "reason": "Business rule validation failed.",
            "validation": validation,
            "products": []
        }

    print("High-value workflow executed!")

    return {
        "status": "SUCCESS",
        "validation": validation,
        "analysis": get_high_value_analysis()
    }


if __name__ == "__main__":
    result = agent.run_sync(
        "Which products are high-value?"
    )

    print("\nFinal answer:")
    print(result.output)

    print("\nModel requests:")
    print(result.usage.requests)


# if __name__ == "__main__":
#     print(get_high_value_analysis())
