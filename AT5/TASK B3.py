
import csv
import sqlite3
import pandas as pd
import time
import cProfile
import pstats
import io
from datetime import datetime, timedelta


# Generate Data for Different Station Counts

def generate_data(station_count, filename):

    start_date = datetime(2026, 1, 1)

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["station", "date", "pm25"])

        for station_no in range(1, station_count + 1):

            station = "Station" + str(station_no)

            for hour in range(365 * 24):

                day = start_date + timedelta(hours=hour)

                pm25 = 30 + (hour % 100)

                writer.writerow([
                    station,
                    day.strftime("%Y-%m-%d"),
                    pm25
                ])


# B3.1 – Method 1: Python CSV Loops

def python_csv(filename):

    totals = {}
    counts = {}

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            key = (row["station"], row["date"])

            value = float(row["pm25"])

            totals[key] = totals.get(key, 0) + value

            counts[key] = counts.get(key, 0) + 1

    result = {
        key: totals[key] / counts[key]
        for key in totals
    }

    return result


# B3.1 – Method 2: Pandas GroupBy

def pandas_groupby(filename):

    df = pd.read_csv(filename)

    result = df.groupby(
        ["station", "date"]
    )["pm25"].mean()

    return result


# B3.1 – Method 3: SQL GROUP BY

def sql_groupby(filename):

    conn = sqlite3.connect(":memory:")

    conn.execute("""
    CREATE TABLE readings (
        station TEXT,
        day TEXT,
        pm25 REAL
    )
    """)

    batch = []

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            batch.append((
                row["station"],
                row["date"],
                float(row["pm25"])
            ))

            if len(batch) == 10000:

                conn.executemany(
                    "INSERT INTO readings VALUES (?, ?, ?)",
                    batch
                )

                batch.clear()

        if batch:

            conn.executemany(
                "INSERT INTO readings VALUES (?, ?, ?)",
                batch
            )

    conn.commit()

    result = conn.execute("""
    SELECT station, day, AVG(pm25)
    FROM readings
    GROUP BY station, day
    """).fetchall()

    conn.close()

    return result


# B3.2 – Measure Execution Time

for count in [1, 12, 120]:

    filename = "data_" + str(count) + ".csv"

    print("\n---", count, "STATIONS ---")

    generate_data(count, filename)

    # Python CSV timing
    start = time.perf_counter()

    csv_result = python_csv(filename)

    csv_time = time.perf_counter() - start

    # Pandas timing
    start = time.perf_counter()

    pandas_result = pandas_groupby(filename)

    pandas_time = time.perf_counter() - start

    # SQL timing
    start = time.perf_counter()

    sql_result = sql_groupby(filename)

    sql_time = time.perf_counter() - start

    print("CSV Time:", round(csv_time, 4), "seconds")

    print("Pandas Time:", round(pandas_time, 4), "seconds")

    print("SQL Time:", round(sql_time, 4), "seconds")

    print("Daily Groups:", len(csv_result))


# B3.1 – Verify Correctness on Small Data

small_file = "data_1.csv"

csv_result = python_csv(small_file)

pandas_result = pandas_groupby(small_file)

sql_result = sql_groupby(small_file)

sql_dictionary = {
    (station, day): average
    for station, day, average in sql_result
}

pandas_dictionary = pandas_result.to_dict()

assert csv_result.keys() == pandas_dictionary.keys()

assert csv_result.keys() == sql_dictionary.keys()

for key in csv_result:

    assert abs(
        csv_result[key] - pandas_dictionary[key]
    ) < 0.000001

    assert abs(
        csv_result[key] - sql_dictionary[key]
    ) < 0.000001

print("\nAll three methods produce matching results.")


# B3.3 – Profile Python CSV Version

print("\n--- CPROFILE RESULT ---")

profiler = cProfile.Profile()

profiler.enable()

python_csv("data_1.csv")

profiler.disable()

stats = pstats.Stats(profiler)

stats.sort_stats("cumulative")

stats.print_stats(10)


# B3.4 – Engineering Trade-Off

print("\n--- ENGINEERING DECISION ---")

print("Python loops are suitable for small datasets.")

print("Pandas is useful for quick data analysis.")

print("SQL is suitable for repeated database queries.")

print("All methods calculate daily averages.")
