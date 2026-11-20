
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Read cleaned data
df = pd.read_csv("cleaned_air_quality.csv")

# Convert date into datetime format
df["date"] = pd.to_datetime(df["date"])

# A3.1 – Choose the Charts

# 1. Line Chart – PM2.5 Trend Over a Month
daily = df.groupby("date")["pm25"].mean()

plt.figure()
daily.plot(kind="line", marker="o")
plt.title("Monthly PM2.5 Trend")
plt.xlabel("Date")
plt.ylabel("Average PM2.5")
plt.grid()
plt.show()

# 2. Bar Chart – Comparison of Stations
station_avg = df.groupby("station_name")["pm25"].mean()

plt.figure()
station_avg.plot(kind="bar")
plt.title("PM2.5 Comparison Between Stations")
plt.xlabel("Station Name")
plt.ylabel("Average PM2.5")
plt.show()

# 3. Scatter Plot – Temperature and PM2.5
plt.figure()
plt.scatter(df["temperature"], df["pm25"])
plt.title("Temperature vs PM2.5")
plt.xlabel("Temperature")
plt.ylabel("PM2.5")
plt.show()

# 4. Bar Chart – Hours with Worst Air Quality
df["hour"] = pd.to_datetime(
    df["time"], format="%H:%M"
).dt.hour

hourly_avg = df.groupby("hour")["pm25"].mean()

plt.figure()
hourly_avg.plot(kind="bar")
plt.title("Average PM2.5 by Hour")
plt.xlabel("Hour")
plt.ylabel("Average PM2.5")
plt.show()


# A3.2 – Daily Summary Table Using SQL

conn = sqlite3.connect("air_quality.db")

# Create daily summary table
query = """
SELECT
    s.station_name,
    r.reading_date,
    MIN(r.pm25) AS minimum,
    MAX(r.pm25) AS maximum,
    AVG(r.pm25) AS mean,
    COUNT(r.pm25) AS valid_readings
FROM readings r
JOIN stations s
ON r.station_id = s.station_id
GROUP BY s.station_name, r.reading_date
ORDER BY s.station_name, r.reading_date
"""

summary = pd.read_sql_query(query, conn)

print("\n--- DAILY SUMMARY TABLE ---")
print(summary)

summary.to_csv("daily_summary.csv", index=False)

conn.close()

print("\nDaily summary saved successfully")


# Alternative Concept – Python Loops

loop_summary = {}

for _, row in df.iterrows():

    key = (row["station_name"], row["date"])

    if key not in loop_summary:
        loop_summary[key] = []

    loop_summary[key].append(row["pm25"])

print("\n--- SUMMARY USING PYTHON LOOPS ---")

for key, values in loop_summary.items():

    print("\nStation and Date:", key)
    print("Minimum:", min(values))
    print("Maximum:", max(values))
    print("Mean:", sum(values) / len(values))
    print("Valid Readings:", len(values))
