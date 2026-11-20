
import random
import time

# Generate 365 rainfall readings
readings = [random.randint(0, 50) for _ in range(365)]

# Weekly totals using slicing
weekly_totals = []
for i in range(0, len(readings), 7):
    weekly_totals.append(sum(readings[i:i+7]))

print("Weekly totals:", weekly_totals)

# Maximum and minimum rainfall
print("Maximum rainfall:", max(readings))
print("Minimum rainfall:", min(readings))
print("Wettest day:", readings.index(max(readings)) + 1)
print("Driest day:", readings.index(min(readings)) + 1)

# 7-day moving average (naive method)
moving_avg = []
for i in range(len(readings) - 6):
    moving_avg.append(sum(readings[i:i+7]) / 7)

print("Moving averages:", moving_avg)

# Dry days
dry_days = [i + 1 for i, value in enumerate(readings) if value == 0]
print("Dry days:", dry_days)

# Running sum method
running_avg = []
window_sum = sum(readings[:7])

for i in range(len(readings) - 6):
    if i > 0:
        window_sum += readings[i+6] - readings[i-1]
    running_avg.append(window_sum / 7)

print("Running sum averages:", running_avg)

# Test empty and short lists
for test in [[], [2, 4, 6]]:
    if len(test) < 7:
        print("Not enough readings for moving average:", test)

# Experiment with different sizes
for n in [365, 36500, 365000]:
    data = [random.randint(0, 50) for _ in range(n)]

    start = time.time()
    naive = [sum(data[i:i+7])/7 for i in range(n-6)]
    naive_time = time.time() - start

    start = time.time()
    total = sum(data[:7])
    result = []
    for i in range(n-6):
        if i > 0:
            total += data[i+6] - data[i-1]
        result.append(total/7)
    running_time = time.time() - start

    print(n, "Naive:", naive_time, "Running:", running_time)
