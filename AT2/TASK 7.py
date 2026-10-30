import time


def ways_naive(n):
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


def ways_memo(n, cache=None):
    if cache is None:
        cache = {}

    if n <= 1:
        return 1

    if n not in cache:
        cache[n] = ways_memo(n - 1, cache) + ways_memo(n - 2, cache)

    return cache[n]


def ways_loop(n):
    if n <= 1:
        return 1

    a, b = 1, 1

    for i in range(2, n + 1):
        a, b = b, a + b

    return b


print("Validation:")
for n in range(1, 7):
    print(
        f"n = {n}: "
        f"naive = {ways_naive(n)}, "
        f"memo = {ways_memo(n)}, "
        f"loop = {ways_loop(n)}"
    )


print("\nPerformance comparison:")

for n in [10, 20, 25, 30]:
    start = time.perf_counter()
    result_naive = ways_naive(n)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    result_memo = ways_memo(n)
    memo_time = time.perf_counter() - start

    start = time.perf_counter()
    result_loop = ways_loop(n)
    loop_time = time.perf_counter() - start

    print(f"\nn = {n}")
    print("Results match:", result_naive == result_memo == result_loop)
    print(f"Naive time: {naive_time:.8f} seconds")
    print(f"Memo time:  {memo_time:.8f} seconds")
    print(f"Loop time:  {loop_time:.8f} seconds")


print("\nFor 1000 steps:")
start = time.perf_counter()
result = ways_loop(1000)
loop_time = time.perf_counter() - start

print("Number of ways:", result)
print(f"Loop time: {loop_time:.8f} seconds")