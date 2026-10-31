HIGH_VALUE_THRESHOLD = 1000


def classify_products(products: list[dict]) -> list[dict]:
    results = []

    for product in products:
        revenue = product["revenue"]

        results.append({
            "product": product["product"],
            "revenue": revenue,
            "is_high_value": revenue > HIGH_VALUE_THRESHOLD
        })

    return results


if __name__ == "__main__":
    products = [
        {"product": "Laptop", "revenue": 2400},
        {"product": "Monitor", "revenue": 900},
        {"product": "Keyboard", "revenue": 350},
        {"product": "Mouse", "revenue": 250}
    ]

    results = classify_products(products)

    for result in results:
        print(result)