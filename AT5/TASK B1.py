
import csv
import io
import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict

# B1.1 – Test Data

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Adyar,2026-10-04,1200
"""

print("--- DATA BEFORE CLEANING ---")
print(RAW)


# Cleaning Function

def load_clean(text):

    rows = []
    reader = csv.DictReader(io.StringIO(text))

    for row in reader:

        value = row["pm25"].strip()

        if value == "" or value.upper() == "NA":
            continue

        try:
            pm25 = float(value)
        except ValueError:
            continue

        if pm25 < 0 or pm25 > 999:
            continue

        rows.append((
            row["station"].strip(),
            row["date"].strip(),
            pm25
        ))

    return rows


# B1.1 – Clean Data

clean = load_clean(RAW)

print("\n--- DATA AFTER CLEANING ---")
print(clean)


# Min-Max Normalisation

def min_max(values):

    if not values:
        return []

    minimum = min(values)
    maximum = max(values)

    if minimum == maximum:
        return [0.0] * len(values)

    return [
        round((v - minimum) / (maximum - minimum), 3)
        for v in values
    ]


print("\nNormalised Values:")
print(min_max([pm for _, _, pm in clean]))


# B1.2 – Compare with Part A Design

print("\nCleaning follows the Part A design.")
print("Missing, negative and above-999 values are removed.")
print("Valid readings are converted into float values.")


# B1.3 – Store Data in SQLite

conn = sqlite3.connect("B1_air_quality.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

cursor.execute("DELETE FROM readings")

cursor.executemany("""
INSERT INTO readings VALUES (?, ?, ?)
""", clean)

conn.commit()

# Question 1 – Average PM2.5 of Adyar
cursor.execute("""
SELECT AVG(pm25)
FROM readings
WHERE station = 'Adyar'
AND day BETWEEN '2026-10-01' AND '2026-10-31'
""")

print("\nAverage PM2.5 of Adyar:", cursor.fetchone()[0])

# Question 2 – Maximum PM2.5
cursor.execute("""
SELECT station, MAX(pm25)
FROM readings
GROUP BY station
""")

print("\nMaximum PM2.5:")
for row in cursor.fetchall():
    print(row)

# Question 3 – Number of Readings
cursor.execute("""
SELECT station, COUNT(*)
FROM readings
GROUP BY station
""")

print("\nNumber of Readings:")
for row in cursor.fetchall():
    print(row)

conn.close()


# B1.4 – Visualisation Without Pandas

chart_data = [
    ("Adyar", "2026-10-01", "08:00", 48, 30),
    ("Adyar", "2026-10-01", "12:00", 55, 32),
    ("Adyar", "2026-10-02", "08:00", 52, 29),
    ("Guindy", "2026-10-01", "08:00", 95, 31),
    ("Guindy", "2026-10-02", "12:00", 85, 33),
    ("Guindy", "2026-10-03", "16:00", 121, 34)
]

# 1. Line Chart – Monthly Trend
daily = defaultdict(list)

for station, date, time, pm, temp in chart_data:
    daily[date].append(pm)

dates = sorted(daily)
averages = [
    sum(daily[d]) / len(daily[d])
    for d in dates
]

plt.figure()
plt.plot(dates, averages, marker="o")
plt.title("Monthly PM2.5 Trend")
plt.xlabel("Date")
plt.ylabel("Average PM2.5")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2. Bar Chart – Station Comparison
station_values = defaultdict(list)

for station, date, time, pm, temp in chart_data:
    station_values[station].append(pm)

stations = list(station_values)
station_avg = [
    sum(station_values[s]) / len(station_values[s])
    for s in stations
]

plt.figure()
plt.bar(stations, station_avg)
plt.title("Station Comparison")
plt.xlabel("Station")
plt.ylabel("Average PM2.5")
plt.show()


# 3. Scatter Plot – Temperature vs PM2.5
temperatures = [row[4] for row in chart_data]
pm_values = [row[3] for row in chart_data]

plt.figure()
plt.scatter(temperatures, pm_values)
plt.title("Temperature vs PM2.5")
plt.xlabel("Temperature")
plt.ylabel("PM2.5")
plt.show()


# 4. Bar Chart – Hourly Air Quality
hour_values = defaultdict(list)

for station, date, time, pm, temp in chart_data:
    hour = int(time.split(":")[0])
    hour_values[hour].append(pm)

hours = sorted(hour_values)
hour_avg = [
    sum(hour_values[h]) / len(hour_values[h])
    for h in hours
]

plt.figure()
plt.bar(hours, hour_avg)
plt.title("Average PM2.5 by Hour")
plt.xlabel("Hour")
plt.ylabel("Average PM2.5")
plt.show()

print("\nB1 completed successfully.")
