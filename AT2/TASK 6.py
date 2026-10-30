from functools import lru_cache
import sys

calls = 0


def ways_naive(n):
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_naive(n - 1) + ways_naive(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_loop(n):
    if n <= 1:
        return 1

    a, b = 1, 1

    for i in range(2, n + 1):
        a, b = b, a + b

    return b


# Check answers for n = 1 to 6
print("Correctness check:")
for n in range(1, 7):
    print(f"n = {n}: {ways_memo(n)} ways")


# Compare naive and memoised function calls
print("\nCall count comparison:")

for n in [10, 20, 25, 30]:
    calls = 0
    ways_naive(n)
    naive_calls = calls

    ways_memo.cache_clear()
    calls = 0
    ways_memo(n)
    memo_calls = calls

    print(f"n = {n}: naive calls = {naive_calls}, memo calls = {memo_calls}")


# Compare results for n = 25
ways_memo.cache_clear()
calls = 0
print("\nnaive:", ways_naive(25), "calls =", calls)

ways_memo.cache_clear()
calls = 0
print("memo :", ways_memo(25), "calls =", calls)


# Recursion limit
print("\nRecursion limit:", sys.getrecursionlimit())

ways_memo.cache_clear()

try:
    print("Memoised ways for 1000 steps:", ways_memo(1000))
except RecursionError:
    print("RecursionError: recursion depth limit exceeded.")


# Iterative solution for 1000 steps
print("Loop result for 1000 steps:", ways_loop(1000))