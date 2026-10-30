import time
import io

def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts):
    return ";".join(parts) + ";" if parts else ""


def build_fstring(parts):
    return "".join(f"{p};" for p in parts)


def build_stringio(parts):
    buffer = io.StringIO()
    for p in parts:
        buffer.write(p + ";")
    return buffer.getvalue()


for n in [1000, 10000, 200000]:
    items = [f"Item{i}:Rs{i % 50}" for i in range(n)]

    plus_times = []
    join_times = []
    fstring_times = []

    for _ in range(3):
        start = time.perf_counter()
        a = build_plus(items)
        plus_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        b = build_join(items)
        join_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        c = build_fstring(items)
        fstring_times.append(time.perf_counter() - start)

    print(f"\nNumber of lines: {n}")
    print("Same text:", a == b == c)
    print(f"Length: {len(b)}")
    print(f"Average += time: {sum(plus_times) / 3:.6f} s")
    print(f"Average join time: {sum(join_times) / 3:.6f} s")
    print(f"Average f-string time: {sum(fstring_times) / 3:.6f} s")