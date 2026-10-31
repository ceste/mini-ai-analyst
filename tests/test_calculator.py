def calculate_revenue(quantity, price):
    return quantity * price

def test_revenue_calculation():
    result = calculate_revenue(3, 300)
    assert result == 900
    # assert result == 1000

def test_zero_quantity():
    result = calculate_revenue(0, 300)
    assert result == 0
