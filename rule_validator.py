from business_rules_rag import retrieve_business_rules
from business_config import HIGH_VALUE_THRESHOLD
import re

# from hybrid_agent import HIGH_VALUE_THRESHOLD


def validate_high_value_rule(document: str) -> dict:
    """Compare a documented threshold with Python's threshold."""

    match = re.search(
        r"more than\s*\$?([\d,]+)",
        document,
        flags=re.IGNORECASE,
    )

    if not match:
        return {
            "status": "UNKNOWN",
            "reason": "Could not identify the documented threshold."
        }

    documented_threshold = int(
        match.group(1).replace(",", "")
    )

    return {
        "status": (
            "MATCH"
            if documented_threshold == HIGH_VALUE_THRESHOLD
            else "CONFLICT"
        ),
        "documented_threshold": documented_threshold,
        "python_threshold": HIGH_VALUE_THRESHOLD,
        "operator": ">"
    }


# if __name__ == "__main__":
#     # document = (
#     #     "A high-value product generates "
#     #     "more than $1000 in revenue."
#     # )

#     document = (
#         "A high-value product generates "
#         "more than $2500 in revenue."
#     )

#     print(validate_high_value_rule(document))



if __name__ == "__main__":

    documents = retrieve_business_rules(
        "What is the definition of a high-value product?"
    )

    print("Retrieved documents:")
    for document in documents:
        print(document)

    matching_rules = [
        document
        for document in documents
        if "high-value product" in document.lower()
    ]

    if len(matching_rules) != 1:
        print({
            "status": "UNKNOWN",
            "reason": "Expected exactly one high-value rule."
        })
    else:
        result = validate_high_value_rule(
            matching_rules[0]
        )

        print("\nValidation result:")
        print(result)
