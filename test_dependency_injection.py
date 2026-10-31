def calculate_revenue(quantity, price):
    return quantity * price


def analyze_sales(quantity, price, calculator):
    revenue = calculator(quantity, price)
    return f"Revenue: {revenue}"


def fake_calculator(quantity, price):
    return 999


print(
    analyze_sales(
        3,
        300,
        calculator=calculate_revenue,
    )
)

print(
    analyze_sales(
        3,
        300,
        calculator=fake_calculator,
    )
)
