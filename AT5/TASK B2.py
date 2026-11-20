
import csv
import io
import sqlite3
import time

# B2 – Create SQLite Database

readings = [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0),
    ("Guindy", "2026-10-03", 121.0),
    ("Adyar", "2026-10-04", 60.0)
]

con = sqlite3.connect(":memory:")

con.execute("""
CREATE TABLE aq (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

# TODO 1 – Insert all readings using executemany()

con.executemany("""
INSERT INTO aq (station, day, pm25)
VALUES (?, ?, ?)
""", readings)

con.commit()


# TODO 2 – Parameterised SQL Query

def station_average(name):

    cursor = con.execute("""
    SELECT AVG(pm25)
    FROM aq
    WHERE station = ?
    """, (name,))

    return cursor.fetchone()[0]


print("--- STATION AVERAGES ---")

print("Adyar:", station_average("Adyar"))
print("Guindy:", station_average("Guindy"))

print("Injection attempt:",
      station_average("Adyar' OR '1'='1"))


# Adversarial File Testing

print("\n--- ADVERSARIAL FILE TESTING ---")

# 1. Missing column
missing_column = """station,day
Adyar,2026-10-01
"""

# 2. Wrong delimiter
wrong_delimiter = """station;day;pm25
Adyar;2026-10-01;48
"""

# 3. Different text encoding
with open("encoding_test.csv", "w", encoding="cp1252") as file:
    file.write("station,day,pm25\nAdyar,2026-10-01,48\n")

# 4. Empty file
with open("empty.csv", "w", encoding="utf-8") as file:
    pass


def test_csv(text):

    reader = csv.DictReader(io.StringIO(text))

    if not reader.fieldnames:
        print("Empty file detected")
        return

    required = {"station", "day", "pm25"}

    if not required.issubset(reader.fieldnames):
        print("Missing column detected")
        return

    if len(reader.fieldnames) == 1:
        print("Wrong delimiter detected")
        return

    print("CSV structure is valid")


test_csv(missing_column)
test_csv(wrong_delimiter)

# Read different encoding
try:
    with open("encoding_test.csv", "r", encoding="utf-8") as file:
        print("Encoding file:", file.read())

except UnicodeDecodeError:
    print("Different encoding detected")

# Read empty file
with open("empty.csv", "r", encoding="utf-8") as file:
    if not file.read().strip():
        print("Empty file detected")


# Compare SQL String Joining and Parameterised Query

print("\n--- SQL INJECTION TEST ---")

malicious_input = "Adyar' OR '1'='1"

# Unsafe SQL query
unsafe_query = (
    "SELECT AVG(pm25) FROM aq WHERE station = '"
    + malicious_input + "'"
)

unsafe_result = con.execute(unsafe_query).fetchone()[0]

print("Unsafe query result:", unsafe_result)

# Safe parameterised query
safe_result = station_average(malicious_input)

print("Safe query result:", safe_result)


# Compare executemany() and execute() in a loop

def insert_with_loop(data):

    start = time.perf_counter()

    for row in data:
        con.execute(
            "INSERT INTO aq VALUES (?, ?, ?)", row
        )

    con.commit()

    return time.perf_counter() - start


def insert_with_many(data):

    start = time.perf_counter()

    con.executemany(
        "INSERT INTO aq VALUES (?, ?, ?)", data
    )

    con.commit()

    return time.perf_counter() - start


sample = [
    ("Adyar", "2026-10-05", 50.0),
    ("Guindy", "2026-10-05", 80.0)
]

loop_time = insert_with_loop(sample)
many_time = insert_with_many(sample)

print("\nExecute loop time:", loop_time)
print("Executemany time:", many_time)

con.close()

print("\nB2 testing completed.")
