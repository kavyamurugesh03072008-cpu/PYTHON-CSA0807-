
import logging
import pdb
import time
import timeit
import cProfile

# A4.1 – Debugging Plan

# Configure logging
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

def clean_pm25(value):

    print("Original value:", value)

    try:
        value = float(value)

        # Check whether the value is valid
        assert value >= 0, "PM2.5 cannot be negative"

        if value > 1000:
            raise ValueError("PM2.5 value is too high")

        logging.info("Valid PM2.5 value: %s", value)

        return round(value, 2)

    except (ValueError, AssertionError) as error:

        logging.error("Cleaning error: %s", error)

        print("Invalid value:", error)

        return None


# Test cleaning function
values = ["45.678", "60", "-5", "abc", "1200"]

cleaned_values = []

for value in values:
    result = clean_pm25(value)
    cleaned_values.append(result)

print("\nCleaned Values:", cleaned_values)


# PDB Debugger
# Remove the comment to debug step by step
# pdb.set_trace()


# A4.2 – Profiling Plan

def calculate_average(numbers):
    return sum(numbers) / len(numbers)


numbers = list(range(1, 10001))

# Using time.perf_counter()
start = time.perf_counter()

result = calculate_average(numbers)

end = time.perf_counter()

print("\nAverage:", result)
print("Execution Time:", end - start)


# Using timeit
execution_time = timeit.timeit(
    lambda: calculate_average(numbers),
    number=100
)

print("Timeit Execution Time:", execution_time)


# Using cProfile
print("\n--- CPROFILE RESULT ---")

cProfile.run("calculate_average(numbers)")


# Alternative – Print Statement Debugging

def test_values(data):

    for value in data:
        print("Checking:", value)

        if value < 0:
            print("Invalid value")
        else:
            print("Valid value")


test_values([10, 20, -5, 30])

print("\nDebugging and profiling completed")
