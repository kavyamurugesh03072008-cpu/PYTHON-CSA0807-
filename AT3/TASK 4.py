
import random
import time

ai_elective = {
    "192311001", "192311004",
    "192311007", "192311009"
}

iot_elective = {
    "192311002", "192311004",
    "192311009", "192311010"
}

all_students = {
    f"1923110{i:02d}" for i in range(1, 11)
}

# TODO 1: Set operations
both = ai_elective & iot_elective

exactly_one = ai_elective ^ iot_elective

neither = all_students - (ai_elective | iot_elective)

print("clash      :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither    :", sorted(neither))

# Using set methods
both2 = ai_elective.intersection(iot_elective)
exactly_one2 = ai_elective.symmetric_difference(iot_elective)
neither2 = all_students.difference(ai_elective.union(iot_elective))

print("\nUsing set methods:")
print(sorted(both2))
print(sorted(exactly_one2))
print(sorted(neither2))

# Duplicate removal
students = ["101", "102", "101", "103", "102"]
unique_students = set(students)
print("Unique students:", sorted(unique_students))

# Membership testing experiment
for n in [10000, 100000, 1000000]:
    data = list(range(n))
    data_set = set(data)

    start = time.time()
    result = n - 1 in data
    list_time = time.time() - start

    start = time.time()
    result = n - 1 in data_set
    set_time = time.time() - start

    print("\nSize:", n)
    print("List search:", list_time)
    print("Set search:", set_time)

# Nested loops vs set intersection
a = set(range(10000))
b = set(range(5000, 15000))

start = time.time()
common = a & b
print("Set intersection time:", time.time() - start)

# Empty and identical sets
empty = set()
print("Empty intersection:", empty & ai_elective)
print("Identical intersection:", ai_elective & ai_elective)
