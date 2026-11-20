
import random
import time
import sys

readings = [2, 5, 60, -55, 7, 9, 4, 100, 3]

# Method 1: Using for loop and append
valid = []
for temp in readings:
    if -50 <= temp <= 50:
        valid.append(temp)

celsius = valid
fahrenheit = []

for temp in celsius:
    fahrenheit.append((temp * 9/5) + 32)

print("Valid Celsius:", celsius)
print("Fahrenheit:", fahrenheit)

# Method 2: List comprehension
valid2 = [temp for temp in readings if -50 <= temp <= 50]

fahrenheit2 = [(temp * 9/5) + 32 for temp in valid2]

print("Comprehension Celsius:", valid2)
print("Comprehension Fahrenheit:", fahrenheit2)

# Method 3: map() and filter()
valid3 = list(filter(lambda x: -50 <= x <= 50, readings))

fahrenheit3 = list(map(lambda x: x * 9/5 + 32, valid3))

print("Filter Celsius:", valid3)
print("Map Fahrenheit:", fahrenheit3)

# Alarm minutes outside 2 to 8 degrees
alarms = [
    minute for minute, temp in enumerate(readings, start=1)
    if -50 <= temp <= 50 and not (2 <= temp <= 8)
]

print("Alarm minutes:", alarms)

# Dictionary comprehension
temperature_dict = {
    i + 1: temp for i, temp in enumerate(readings)
    if -50 <= temp <= 50
}
print("Temperature dictionary:", temperature_dict)

# Set comprehension
temperature_set = {
    temp for temp in readings if -50 <= temp <= 50
}
print("Temperature set:", temperature_set)

# Generator expression
generator = (temp for temp in readings if -50 <= temp <= 50)
print("Generator values:", list(generator))

# Experimental investigation
for n in [10000, 100000, 1000000]:
    data = [random.uniform(-60, 60) for _ in range(n)]

    start = time.time()
    result1 = [x for x in data if -50 <= x <= 50]
    t1 = time.time() - start

    start = time.time()
    result2 = list(filter(lambda x: -50 <= x <= 50, data))
    t2 = time.time() - start

    start = time.time()
    result3 = []
    for x in data:
        if -50 <= x <= 50:
            result3.append(x)
    t3 = time.time() - start

    print("\nReadings:", n)
    print("Comprehension:", t1)
    print("Filter:", t2)
    print("For loop:", t3)

# Memory comparison
my_list = [x for x in range(1000)]
my_generator = (x for x in range(1000))

print("List memory:", sys.getsizeof(my_list))
print("Generator memory:", sys.getsizeof(my_generator))

# All valid and all invalid
print([x for x in [3, 4, 5] if -50 <= x <= 50])
print([x for x in [60, 70, 80] if -50 <= x <= 50])
