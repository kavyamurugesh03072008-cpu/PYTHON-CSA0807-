
import time
from decimal import Decimal, ROUND_HALF_UP

SIZES = [300, 6000, 150000]


def calculate_float(n):
    total = 0.0
    for _ in range(n):
        total += 283.90
    return total


def calculate_decimal(n):
    total = Decimal("0.00")
    payment = Decimal("283.90")

    for _ in range(n):
        total += payment

    return total


def measure(function, n):
    start = time.perf_counter()
    result = function(n)
    elapsed = time.perf_counter() - start
    return result, elapsed


print("FLOAT VS DECIMAL COMPARISON")
print("-" * 50)

for n in SIZES:
    float_total, float_time = measure(calculate_float, n)
    decimal_total, decimal_time = measure(calculate_decimal, n)

    difference = abs(Decimal(str(float_total)) - decimal_total)

    print(f"\nNumber of payments: {n}")
    print(f"Float total:   Rs. {float_total:.2f}")
    print(f"Decimal total: Rs. {decimal_total:.2f}")
    print(f"Difference:    Rs. {difference}")
    print(f"Float time:    {float_time:.6f} seconds")
    print(f"Decimal time:  {decimal_time:.6f} seconds")


def round_each_payment(payments):
    total = Decimal("0.00")

    for payment in payments:
        amount = Decimal(str(payment)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        total += amount

    return total


def round_final_total(payments):
    total = sum(Decimal(str(p)) for p in payments)

    return total.quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


payments = [10.005, 20.005, 30.005]

print("\nROUNDING COMPARISON")
print("Round each payment:", round_each_payment(payments))
print("Round final total: ", round_final_total(payments))


def rate_per_litre(fat, snf):
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    return round(
        30 + fat_steps * 0.40 + snf_steps * 0.30, 2
    )


def recalculate_entries(entries):
    total = 0.0

    for litres, fat, snf in entries:
        rate = rate_per_litre(fat, snf)
        total += round(litres * rate, 2)

    return total


def rate_table_calculation(entries):
    rate_table = {}
    total = 0.0

    for litres, fat, snf in entries:
        key = (fat, snf)

        if key not in rate_table:
            rate_table[key] = rate_per_litre(fat, snf)

        total += round(litres * rate_table[key], 2)

    return total, len(rate_table)


entries = [
    (8.5, 4.2, 8.7),
    (10, 3.5, 8.5),
    (12, 3.1, 8.3)
] * 5000

start = time.perf_counter()
normal_total = recalculate_entries(entries)
normal_time = time.perf_counter() - start

start = time.perf_counter()
table_total, unique_pairs = rate_table_calculation(entries)
table_time = time.perf_counter() - start

print("\nRATE TABLE COMPARISON")
print("Recalculated total:", round(normal_total, 2))
print("Rate table total:  ", round(table_total, 2))
print("Unique fat/SNF pairs:", unique_pairs)
print(f"Recalculation time: {normal_time:.6f} seconds")
print(f"Rate table time:    {table_time:.6f} seconds")
