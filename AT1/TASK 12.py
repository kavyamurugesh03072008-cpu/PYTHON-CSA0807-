
from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")

SEASONAL_BASE_RATE = Decimal("32.00")
SEASONAL_FAT_STEP_VALUE = Decimal("0.45")
BONUS_PER_LITRE = Decimal("0.50")

CENT = Decimal("0.01")
STEP = Decimal("0.1")


def rounded(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def count_steps(value, standard):
    difference = Decimal(str(value)) - Decimal(str(standard))
    return (difference / STEP).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )


def rate_per_litre(fat, snf, month):
    if month in (4, 5, 6):
        base = SEASONAL_BASE_RATE
        fat_value = SEASONAL_FAT_STEP_VALUE
    else:
        base = BASE_RATE
        fat_value = FAT_STEP_VALUE

    fat_steps = count_steps(fat, "3.50")
    snf_steps = count_steps(snf, "8.50")

    rate = (
        base
        + fat_steps * fat_value
        + snf_steps * SNF_STEP_VALUE
    )

    return rounded(rate)


def payout(litres, fat, snf, month):
    litres = Decimal(str(litres))

    if litres <= 0 or Decimal(str(fat)) < 0 or Decimal(str(snf)) < 0:
        raise ValueError("Invalid milk entry")

    rate = rate_per_litre(fat, snf, month)
    return rounded(litres * rate)


def ten_day_total(entries, month):
    total_litres = Decimal("0")
    total_payment = Decimal("0.00")

    for litres, fat, snf in entries:
        litres = Decimal(str(litres))
        payment = payout(litres, fat, snf, month)

        total_litres += litres
        total_payment += payment

    bonus = Decimal("0.00")

    if total_litres > Decimal("500"):
        bonus = rounded(total_litres * BONUS_PER_LITRE)

    return rounded(total_payment), bonus, rounded(total_payment + bonus)


if __name__ == "__main__":
    entries = [
        ("10", "3.50", "8.50"),
        ("8.5", "4.23", "8.67"),
        ("12", "3.10", "8.30")
    ]

    for month in (3, 4):
        print("\nMonth:", month)

        for litres, fat, snf in entries:
            rate = rate_per_litre(fat, snf, month)
            payment = payout(litres, fat, snf, month)
            print(
                f"Litres={litres}, Fat={fat}, SNF={snf}, "
                f"Rate=Rs.{rate:.2f}, Payment=Rs.{payment:.2f}"
            )

    # Bonus tests
    test_entries = [
        ("200", "3.50", "8.50"),
        ("180", "3.50", "8.50"),
        ("130", "3.50", "8.50")
    ]

    base, bonus, final = ten_day_total(test_entries, 4)
    print("\nTotal litres: 510")
    print(f"Payment before bonus: Rs.{base:.2f}")
    print(f"Bonus: Rs.{bonus:.2f}")
    print(f"Final payment: Rs.{final:.2f}")
