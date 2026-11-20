
import copy
import sys
import time

# Tuple as dictionary key
stops = {
    (13.0827, 80.2707): "Chennai Central",
    (13.0418, 80.2341): "T. Nagar"
}

print(stops[(13.0418, 80.2341)])

# Incorrect grid
rows, cols = 3, 4
bad = [[0] * cols] * rows
bad[0][1] = 7

# Correct grid using list comprehension
good = [[0 for j in range(cols)] for i in range(rows)]
good[0][1] = 7

print("bad :", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])

# Aliasing
a = [1, 2, 3]
b = a
b[0] = 10
print("Aliasing:", a)

# Shallow copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
shallow[0][0] = 99
print("Original after shallow copy:", original)

# Deep copy
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print("Original after deep copy:", original)

# Tuple unpacking
coordinates = [(10, 20), (30, 40), (50, 60)]
for latitude, longitude in coordinates:
    print(latitude, longitude)

# Memory comparison
list_data = list(range(1000000))
tuple_data = tuple(range(1000000))

print("List memory:", sys.getsizeof(list_data))
print("Tuple memory:", sys.getsizeof(tuple_data))

# Timing creation and indexing
start = time.time()
my_list = list(range(1000000))
print("List creation:", time.time() - start)

start = time.time()
my_tuple = tuple(range(1000000))
print("Tuple creation:", time.time() - start)

start = time.time()
print(my_list[500000])
print("List indexing:", time.time() - start)

start = time.time()
print(my_tuple[500000])
print("Tuple indexing:", time.time() - start)

# List inside tuple
t = ([1, 2, 3], 4)
t[0].append(5)
print(t)
