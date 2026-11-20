
import random
import time
from collections import Counter

calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received"
]

STOP = {"not", "high"}

# TODO 1: Count word frequencies
def frequencies(texts, stop):
    counts = {}

    for text in texts:
        words = text.lower().split()

        for word in words:
            word = word.strip(".,!?")
            if word and word not in stop:
                counts[word] = counts.get(word, 0) + 1

    return counts

# TODO 2: Find top k words
def top(counts, k):
    return sorted(counts.items(),
                  key=lambda x: (-x[1], x[0]))[:k]

result = frequencies(calls, STOP)
print("Word frequencies:", result)
print("Top 3 words:", top(result, 3))

# Group complaints by district
complaints = [
    ("Chennai", "Seeds not received"),
    ("Madurai", "Fertiliser price high"),
    ("Chennai", "Water shortage"),
    ("Salem", "Crop damage")
]

districts = {}

for district, complaint in complaints:
    districts.setdefault(district, []).append(complaint)

print("District complaints:", districts)

# Experimental investigation
for n in [1000, 10000, 100000]:
    data = [
        random.choice(["seeds", "water", "price", "crop", "fertiliser"])
        for _ in range(n)
    ]

    start = time.time()
    dictionary = {}
    for word in data:
        dictionary[word] = dictionary.get(word, 0) + 1
    dict_time = time.time() - start

    start = time.time()
    counter = Counter(data)
    counter_time = time.time() - start

    start = time.time()
    distinct = set(data)
    list_counts = {word: data.count(word) for word in distinct}
    list_time = time.time() - start

    print("\nComplaints:", n)
    print("Dictionary time:", dict_time)
    print("Counter time:", counter_time)
    print("List.count time:", list_time)

# Empty text and case testing
print(frequencies(["", "SEEDS seeds Seeds!"], STOP))
