import asyncio

from llm import choose_action
from models import ToolDecision


TEST_CASES = [
    (
        "What is Python?",
        "DIRECT"
    ),
    (
        "Which product has the highest revenue?",
        "GET_PRODUCT_REVENUE"
    ),
    (
        "How much revenue did Mouse generate?",
        "GET_PRODUCT_REVENUE"
    ),
    (
        "What is our total revenue?",
        "GET_TOTAL_REVENUE"
    ),
    (
        "Did we make more than $3000 in total?",
        "GET_TOTAL_REVENUE"
    ),
    (
        "What is the combined revenue from all products?",
        "GET_TOTAL_REVENUE"
    ),
]


async def main():

    correct = 0

    for question, expected in TEST_CASES:

        raw = await choose_action(question)

        try:
            decision = ToolDecision.model_validate_json(raw)
            actual = decision.action

        except Exception:
            actual = "INVALID"

        passed = actual == expected

        if passed:
            correct += 1

        print(
            f"{'PASS' if passed else 'FAIL'} | "
            f"expected={expected} | "
            f"actual={actual} | "
            f"{question}"
        )

    print()
    print(f"Score: {correct}/{len(TEST_CASES)}")


asyncio.run(main())