def normalise(text):
    text = text.strip()
    text = text.replace(" ", "")
    text = text.replace("-", "")
    return text.upper()


def is_valid(reg):
    if len(reg) not in (9, 10):
        return False

    if not reg[0:2].isalpha():
        return False

    if not reg[2:4].isdigit():
        return False

    if not reg[4:-4].isalpha():
        return False

    if len(reg[4:-4]) not in (1, 2):
        return False

    if not reg[-4:].isdigit():
        return False

    return True


def format_reg(reg):
    if not is_valid(reg):
        return "INVALID"

    return (
        reg[0:2] + " " +
        reg[2:4] + " " +
        reg[4:-4] + " " +
        reg[-4:]
    )


test_inputs = [
    "tn 09 ab 1234",
    "KA-01-M-0007",
    "TN9AB1234",
    "TN 22 1234 AB",
    "MH 12 XYZ 5678",
    "AP-39-C-4567"
]

for raw in test_inputs:
    reg = normalise(raw)

    print(
        f"{raw:18} -> {reg:11} "
        f"{'valid' if is_valid(reg) else 'INVALID'}"
    )

    if is_valid(reg):
        print("Receipt:", format_reg(reg))