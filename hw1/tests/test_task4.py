from task4 import calculate_discount

def test_calculate_discount():
    assert calculate_discount(100, 10) == 90.5
    assert calculate_discount(10.5, 1) == 10.395
    assert calculate_discount(100, 2.5) == 97.5