
import sqlite3
import time
import re
import random
from collections import Counter

# B4.1 – Sentiment Analysis

POSITIVE = {
    "good", "clean", "fast", "helpful", "improved"
}

NEGATIVE = {
    "bad", "dirty", "slow", "rude", "smoke", "broken"
}

NEGATORS = {"not", "never", "no"}


# TODO 1 – Complete Sentiment Scorer

def score(text):

    words = re.findall(r"[a-zA-Z]+", text.lower())

    total = 0

    for i, word in enumerate(words):

        if word in POSITIVE:
            value = 1

        elif word in NEGATIVE:
            value = -1

        else:
            value = 0

        if i > 0 and words[i - 1] in NEGATORS:
            value = -value

        total += value

    return total


def label(text):

    s = score(text)

    if s > 0:
        return "positive"

    elif s < 0:
        return "negative"

    else:
        return "neutral"


# Test the given examples

print("--- SENTIMENT TEST ---")

tests = [
    "Roads are clean and the bus was fast.",
    "Smoke from the factory, air is bad.",
    "The staff were not helpful.",
    "Not bad, service improved."
]

for complaint in tests:
    print(label(complaint), "|", complaint)


# 50 Citizen Complaints

complaints = [
    "The roads are clean and the buses are fast.",
    "The air quality is bad because of smoke.",
    "The staff are helpful and the service is good.",
    "The roads are dirty and broken.",
    "The bus service is slow.",
    "The park is clean and good.",
    "The factory smoke is bad.",
    "The staff are rude.",
    "The roads have improved.",
    "The public transport is fast.",
    "The area is dirty and polluted.",
    "The service is not good.",
    "The roads are not clean.",
    "The workers are helpful.",
    "The bus service is not slow.",
    "The air is clean.",
    "The road is broken.",
    "The staff are not rude.",
    "The pollution problem is bad.",
    "The transport service is improved.",
    "The streets are clean.",
    "The buses are slow and dirty.",
    "The service is good and helpful.",
    "The factory smoke is harmful.",
    "The road repair is improved.",
    "The staff are not helpful.",
    "The bus is fast.",
    "The environment is clean.",
    "The roads are bad.",
    "The service is not bad.",
    "The park is dirty.",
    "The staff are helpful.",
    "The air quality is good.",
    "The roads are broken and dirty.",
    "The bus service is improved.",
    "The factory produces smoke.",
    "The public service is slow.",
    "The roads are clean and improved.",
    "The staff are rude and unhelpful.",
    "The air quality is not good.",
    "The transport is fast and good.",
    "The streets are dirty.",
    "The service is helpful.",
    "The roads are not broken.",
    "The air is bad.",
    "The park is clean.",
    "The bus service is slow.",
    "The staff are good.",
    "The road is not clean.",
    "The environment is improved."
]

# Manually assigned labels for comparison
human_labels = [
    "positive", "negative", "positive", "negative", "negative",
    "positive", "negative", "negative", "positive", "positive",
    "negative", "negative", "negative", "positive", "positive",
    "positive", "negative", "positive", "negative", "positive",
    "positive", "negative", "positive", "negative", "positive",
    "negative", "positive", "positive", "negative", "positive",
    "negative", "positive", "positive", "negative", "positive",
    "negative", "negative", "positive", "negative", "negative",
    "positive", "negative", "positive", "positive", "negative",
    "positive", "negative", "positive", "negative", "positive"
]

correct = 0

print("\n--- 50 COMPLAINT RESULTS ---")

for i, complaint in enumerate(complaints):

    predicted = label(complaint)

    actual = human_labels[i]

    if predicted == actual:
        correct += 1

    print(
        i + 1,
        predicted,
        "| Actual:",
        actual
    )

accuracy = correct / len(complaints) * 100

print("\nTotal Complaints:", len(complaints))
print("Correct Predictions:", correct)
print("Agreement Percentage:", round(accuracy, 2), "%")


# Extractive Complaint Summariser

def summarize(text, k=2):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    words = re.findall(r"[a-zA-Z]+", text.lower())

    stop_words = {
        "the", "is", "a", "an", "and",
        "of", "in", "to", "for", "are"
    }

    important_words = [
        word for word in words
        if word not in stop_words
    ]

    frequency = Counter(important_words)

    scored_sentences = []

    for position, sentence in enumerate(sentences):

        sentence_words = re.findall(
            r"[a-zA-Z]+",
            sentence.lower()
        )

        sentence_score = sum(
            frequency[word] for word in sentence_words
        )

        scored_sentences.append(
            (sentence_score, position, sentence)
        )

    selected = sorted(
        scored_sentences,
        key=lambda item: item[0],
        reverse=True
    )[:k]

    # Keep original sentence order
    selected.sort(key=lambda item: item[1])

    return " ".join(item[2] for item in selected)


combined_text = " ".join(complaints)

print("\n--- COMPLAINT SUMMARY ---")
print(summarize(combined_text, 5))


# Alternative – First Five Sentences

def first_sentences(text, k=5):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return " ".join(sentences[:k])


print("\n--- FIRST FIVE SENTENCES ---")
print(first_sentences(combined_text, 5))


# B4.2 – Check Database and Add Index

conn = sqlite3.connect("B4_air_quality.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

cursor.execute("DELETE FROM readings")

# Generate sample database records
random.seed(10)

data = []

for station_no in range(1, 101):

    station = "Station" + str(station_no)

    for day_no in range(1, 101):

        for reading_no in range(10):

            pm25 = random.randint(20, 150)

            data.append((
                station,
                "2026-10-" + str((day_no - 1) % 30 + 1).zfill(2),
                pm25
            ))

cursor.executemany("""
INSERT INTO readings VALUES (?, ?, ?)
""", data)

conn.commit()


# Measure Query Before Index

query = """
SELECT AVG(pm25)
FROM readings
WHERE station = ? AND day = ?
"""

start = time.perf_counter()

for i in range(100):

    cursor.execute(
        query,
        ("Station50", "2026-10-10")
    )

    cursor.fetchone()

before_index = time.perf_counter() - start

print("\nQuery Time Before Index:", before_index)


# Create Index

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_station_day
ON readings(station, day)
""")

conn.commit()


# Measure Query After Index

start = time.perf_counter()

for i in range(100):

    cursor.execute(
        query,
        ("Station50", "2026-10-10")
    )

    cursor.fetchone()

after_index = time.perf_counter() - start

print("Query Time After Index:", after_index)


# Display Query Plan

print("\n--- QUERY PLAN ---")

cursor.execute("""
EXPLAIN QUERY PLAN
SELECT AVG(pm25)
FROM readings
WHERE station = 'Station50'
AND day = '2026-10-10'
""")

for row in cursor.fetchall():
    print(row)


conn.close()


# B4.3 – Final Engineering Decision

print("\n--- FINAL ENGINEERING DECISION ---")

print("Use SQLite for structured air quality readings.")

print("Use indexed queries for faster data retrieval.")

print("Use automated cleaning to remove invalid readings.")

print("Use sentiment analysis to classify citizen complaints.")

print("Use a trained model for complex complaint analysis.")

print("Generate daily reports using SQL and Python.")

print("\nB4 completed successfully.")
