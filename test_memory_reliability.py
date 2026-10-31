# from conversation_memory import initialize_memory
from semantic_memory import search_memory


from app.memory.conversation_memory import (
    initialize_memory,
    save_fact,
    load_fact
)

initialize_memory()

test_cases = [
    (
        "What's our high-value revenue threshold?",
        "high_value_threshold"
    ),
    (
        "What's the minimum revenue for a high-value product?",
        "high_value_threshold"
    ),
    (
        "How do we calculate product revenue?",
        "revenue_formula"
    ),
    (
        "How much money does a product generate from its quantity and price?",
        "revenue_formula"
    ),
    (
        "Who is our CEO?",
        None
    )
]

passed = 0

for question, expected_key in test_cases:

    result = search_memory(question)

    actual_key = (
        result["key"]
        if result is not None
        else None
    )

    success = actual_key == expected_key

    if success:
        passed += 1

    print("\nQuestion:", question)
    print("Expected:", expected_key)
    print("Actual:", actual_key)
    print("Result:", "PASS" if success else "FAIL")

accuracy = passed / len(test_cases)

print("\n------------------------")
print(f"Passed: {passed}/{len(test_cases)}")
print(f"Accuracy: {accuracy:.1%}")
