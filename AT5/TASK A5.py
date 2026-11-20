
import re
import sqlite3
from collections import Counter

# A5.1 – Sentiment Analysis

positive_words = [
    "good", "excellent", "clean", "helpful",
    "improved", "safe", "better"
]

negative_words = [
    "bad", "poor", "dirty", "dangerous",
    "problem", "worst", "pollution"
]


def sentiment_score(text):

    words = text.lower().split()
    score = 0

    for i, word in enumerate(words):

        if word in positive_words:

            if i > 0 and words[i - 1] == "not":
                score -= 1
            else:
                score += 1

        elif word in negative_words:

            if i > 0 and words[i - 1] == "not":
                score += 1
            else:
                score -= 1

    if score > 0:
        return "Positive"

    elif score < 0:
        return "Negative"

    else:
        return "Neutral"


complaint = "The air quality is not good and pollution is bad"

print("--- SENTIMENT ANALYSIS ---")
print("Complaint:", complaint)
print("Sentiment:", sentiment_score(complaint))


# Extractive Text Summarisation

def summarize_text(text):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    stop_words = {
        "the", "is", "a", "an", "and", "of",
        "in", "to", "for", "on", "it"
    }

    important_words = [
        word for word in words
        if word not in stop_words
    ]

    frequency = Counter(important_words)

    sentence_scores = {}

    for sentence in sentences:

        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b',
            sentence.lower()
        )

        score = sum(
            frequency[word]
            for word in sentence_words
        )

        sentence_scores[sentence] = score

    summary = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )

    return " ".join(summary[:2])


text = """
The air quality in our area is very poor.
People are facing pollution problems.
The authorities should improve air quality.
"""

print("\n--- COMPLAINT SUMMARY ---")
print(summarize_text(text))


# A5.2 – Rule-Based Chatbot

def air_quality_chatbot(question):

    question = question.lower()

    stations = ["adyar", "velachery", "guindy"]

    if "pm2.5" in question or "pm25" in question:

        station = None

        for name in stations:
            if name in question:
                station = name.title()
                break

        if station is None:
            return "Please specify a station name."

        try:
            conn = sqlite3.connect("air_quality.db")
            cursor = conn.cursor()

            cursor.execute("""
            SELECT AVG(r.pm25)
            FROM readings r
            JOIN stations s
            ON r.station_id = s.station_id
            WHERE s.station_name = ?
            AND r.reading_date = DATE('now', 'localtime')
            """, (station,))

            result = cursor.fetchone()[0]

            conn.close()

            if result is None:
                return "No readings available for this station today."

            return (
                f"The average PM2.5 in {station} today "
                f"is {result:.2f}."
            )

        except sqlite3.Error:
            return "Unable to access the air quality database."

    elif "help" in question:
        return "You can ask about PM2.5 levels at monitoring stations."

    else:
        return "Sorry, I cannot understand your question."


# Test Chatbot
print("\n--- CITIZEN CHATBOT ---")

question = "What is the PM2.5 in Adyar today?"

print("Citizen:", question)
print("Chatbot:", air_quality_chatbot(question))


# Alternative Concept – Machine Learning Sentiment Analysis

# Install scikit-learn before running this section:
# pip install scikit-learn

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

complaints = [
    "The air quality is good",
    "The environment is clean",
    "The air quality is very poor",
    "Pollution is dangerous",
    "The service is helpful",
    "The pollution problem is bad"
]

labels = [
    "Positive",
    "Positive",
    "Negative",
    "Negative",
    "Positive",
    "Negative"
]

model = make_pipeline(
    CountVectorizer(),
    MultinomialNB()
)

model.fit(complaints, labels)

new_complaint = ["The air quality is very poor"]

prediction = model.predict(new_complaint)

print("\n--- MACHINE LEARNING RESULT ---")
print("Predicted Sentiment:", prediction[0])
