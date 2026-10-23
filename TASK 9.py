def calculate_payment(quantity, fat, snf):
    try:
        quantity = float(quantity)
        fat = float(fat)
        snf = float(snf)
    except (ValueError, TypeError):
        raise ValueError("Inputs must be numeric")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    if not 3.0 <= fat <= 6.0:
        raise ValueError("Fat must be between 3.0% and 6.0%")

    if snf < 0:
        raise ValueError("SNF cannot be negative")

    rate = (fat * 10) + (snf * 2)
    return round(quantity * rate, 2)


# Automated tests using assert statements
tests = [
    ("Below standard", 10, 3.2, 8.0, 480.00),
    ("Fat above, SNF below", 12, 4.2, 8.2, 700.80),
    ("Fat below, SNF above", 8, 3.3, 9.0, 408.00),
    ("Both above standard", 15, 4.0, 9.0, 870.00),
    ("Exact standard values", 10, 3.5, 8.5, 520.00),
    ("Lowest allowed fat", 10, 3.0, 8.5, 470.00),
    ("Highest allowed fat", 10, 6.0, 8.5, 770.00),
]

for name, q, fat, snf, expected in tests:
    actual = calculate_payment(q, fat, snf)
    assert actual == expected, f"{name}: expected {expected}, got {actual}"
    print(f"{name}: PASS | Payment = {actual:.2f}")


# Invalid input tests
invalid_tests = [
    ("Text input", ("abc", 3.5, 8.5)),
    ("Negative quantity", (-5, 3.5, 8.5)),
    ("Fat below range", (10, 2.9, 8.5)),
    ("Fat above range", (10, 6.1, 8.5)),
]

for name, values in invalid_tests:
    try:
        calculate_payment(*values)
        assert False, f"{name}: should raise ValueError"
    except ValueError:
        print(f"{name}: PASS | Invalid input rejected")


print("All tests completed successfully.")
