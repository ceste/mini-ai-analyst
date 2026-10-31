
from business_logic import classify_products


def run_classification(products: list[dict]):
    return classify_products(products)


# Only tools explicitly registered here can be called.
ALLOWED_TOOLS = {
    "classify_products": run_classification,
}


def execute_tool(tool_name: str, arguments: dict):
    if tool_name not in ALLOWED_TOOLS:
        raise ValueError(f"Tool not allowed: {tool_name}")

    if tool_name == "classify_products":
        if set(arguments) != {"products"}:
            raise ValueError("Expected only the 'products' argument")

        products = arguments["products"]

        if not isinstance(products, list):
            raise ValueError("'products' must be a list")

        if len(products) > 100:
            raise ValueError("Too many products")

        for product in products:
            if not isinstance(product, dict):
                raise ValueError("Invalid product")

            if set(product) != {"product", "revenue"}:
                raise ValueError("Invalid product fields")

            if not isinstance(product["product"], str):
                raise ValueError("Invalid product name")

            revenue = product["revenue"]
            if type(revenue) not in (int, float):
                raise ValueError("Invalid revenue")

            if not 0 <= revenue <= 1_000_000_000:
                raise ValueError("Revenue out of range")

    return ALLOWED_TOOLS[tool_name](**arguments)


if __name__ == "__main__":
    products = [
        {"product": "Laptop", "revenue": 2400},
        {"product": "Monitor", "revenue": 900},
    ]

    # Allowed request
    result = execute_tool(
        "classify_products",
        {"products": products}
    )
    print("Allowed result:", result)

    # Disallowed request
    try:
        execute_tool(
            "delete_database",
            {}
        )
    except ValueError as error:
        print("Blocked:", error)
