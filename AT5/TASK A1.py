
import csv
import sqlite3
import pandas as pd

# A1.1 – Inspect the Source CSV File

def inspect_csv(filename):
    print("\n--- CSV FILE INSPECTION ---")

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        print("CSV Columns:", reader.fieldnames)

        for row_no, row in enumerate(reader, start=2):

            print("Row", row_no, ":", row)

            if not row.get("station_name"):
                print("Missing station name")

            if not row.get("date"):
                print("Missing date")

            if not row.get("pm25"):
                print("Missing PM2.5 value")

            try:
                float(row["pm25"])
            except (ValueError, TypeError):
                print("Invalid PM2.5 value")

            try:
                float(row["temperature"])
            except (ValueError, TypeError):
                print("Invalid temperature")


# A1.2 – Design the SQLite Database

def create_database():
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        station_id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_name TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER,
        reading_date TEXT,
        reading_time TEXT,
        pm25 REAL,
        temperature REAL,
        FOREIGN KEY (station_id)
        REFERENCES stations(station_id),
        UNIQUE(station_id, reading_date, reading_time)
    )
    """)

    conn.commit()
    conn.close()

    print("\nDatabase created successfully")


# A1.3 – Insert CSV Data into SQLite

def insert_csv(filename):
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute("""
            INSERT OR IGNORE INTO stations (station_name)
            VALUES (?)
            """, (row["station_name"],))

            cursor.execute("""
            SELECT station_id FROM stations
            WHERE station_name = ?
            """, (row["station_name"],))

            station_id = cursor.fetchone()[0]

            try:
                cursor.execute("""
                INSERT OR IGNORE INTO readings
                (station_id, reading_date, reading_time,
                 pm25, temperature)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    station_id,
                    row["date"],
                    row["time"],
                    float(row["pm25"]),
                    float(row["temperature"])
                ))

            except (ValueError, TypeError):
                print("Invalid reading skipped:", row)

    conn.commit()
    conn.close()

    print("CSV data inserted successfully")


# Answering Board Questions Using SQL

def analyse_data():
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()

    # Question 1: Average PM2.5 of Adyar in October
    cursor.execute("""
    SELECT AVG(r.pm25)
    FROM readings r
    JOIN stations s
    ON r.station_id = s.station_id
    WHERE s.station_name = 'Adyar'
    AND r.reading_date BETWEEN
    '2026-10-01' AND '2026-10-31'
    """)

    print("\nAverage PM2.5:", cursor.fetchone()[0])

    # Question 2: Maximum PM2.5 at each station
    cursor.execute("""
    SELECT s.station_name, MAX(r.pm25)
    FROM readings r
    JOIN stations s
    ON r.station_id = s.station_id
    GROUP BY s.station_name
    """)

    print("\nMaximum PM2.5:")
    for row in cursor.fetchall():
        print(row)

    # Question 3: Number of readings at each station
    cursor.execute("""
    SELECT s.station_name, COUNT(*)
    FROM readings r
    JOIN stations s
    ON r.station_id = s.station_id
    GROUP BY s.station_name
    """)

    print("\nNumber of Readings:")
    for row in cursor.fetchall():
        print(row)

    conn.close()


# Alternative: Answer Questions Using Pandas and CSV

def analyse_csv(filename):
    df = pd.read_csv(filename)

    print("\n--- PANDAS ANALYSIS ---")

    print("Average PM2.5:", df["pm25"].mean())

    print("Maximum PM2.5:", df["pm25"].max())

    print("Total Readings:", len(df))


# Main Program

filename = "Adyar.csv"

inspect_csv(filename)

create_database()

insert_csv(filename)

analyse_data()

analyse_csv(filename)
