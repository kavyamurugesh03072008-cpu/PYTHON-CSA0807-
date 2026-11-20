
import random
import time
import sys

# Nested dictionary containing 5 trains
trains = {
    101: {
        "name": "Chennai Express",
        "stops": [
            ("Chennai", "06:00", "06:10"),
            ("Katpadi", "08:00", "08:05"),
            ("Bangalore", "11:00", "11:10")
        ],
        "days": {"Monday", "Tuesday", "Wednesday"}
    },

    102: {
        "name": "Pandian Express",
        "stops": [
            ("Chennai", "07:00", "07:15"),
            ("Madurai", "13:00", "13:10")
        ],
        "days": {"Monday", "Friday"}
    },

    103: {
        "name": "Coimbatore Express",
        "stops": [
            ("Chennai", "08:00", "08:10"),
            ("Salem", "11:00", "11:05"),
            ("Coimbatore", "14:00", "14:10")
        ],
        "days": {"Tuesday", "Thursday"}
    },

    104: {
        "name": "Mysore Express",
        "stops": [
            ("Chennai", "09:00", "09:10"),
            ("Katpadi", "11:00", "11:05"),
            ("Mysore", "15:00", "15:10")
        ],
        "days": {"Monday", "Wednesday"}
    },

    105: {
        "name": "Kanyakumari Express",
        "stops": [
            ("Chennai", "10:00", "10:10"),
            ("Trichy", "14:00", "14:05"),
            ("Madurai", "16:00", "16:10")
        ],
        "days": {"Friday", "Saturday"}
    }
}

# Find trains at a station on a given day
station = "Katpadi"
day = "Monday"

results = []

for number, details in trains.items():
    if day in details["days"]:
        for stop, arrival, departure in details["stops"]:
            if stop == station:
                results.append(
                    (number, details["name"], arrival, departure)
                )

# Sort by departure time
results = sorted(results, key=lambda x: x[3])

print("Trains at", station, "on", day)

for train in results:
    print(train)

# Print complete timetable
print("\nComplete Timetable")

for number, details in trains.items():
    print("\nTrain:", number, details["name"])
    print("Running days:", details["days"])

    for station, arrival, departure in details["stops"]:
        print(station, arrival, departure)

# Create station index
station_index = {}

for number, details in trains.items():
    for stop, arrival, departure in details["stops"]:
        station_index.setdefault(stop, []).append(number)

print("\nStation Index:", station_index)

# Fast station search using index
search_station = "Madurai"

print("Trains stopping at", search_station,
      ":", station_index.get(search_station, []))

# Unknown station test
print("Unknown station:", station_index.get("Mumbai", []))

# Experimental investigation
for n in [100, 1000, 10000]:

    timetable = {}

    for i in range(n):
        timetable[i] = {
            "stops": [
                (random.choice(["Chennai", "Salem", "Madurai"]),
                 "10:00", "10:10")
            ],
            "days": {"Monday"}
        }

    # Search without index
    start = time.time()

    for number, details in timetable.items():
        for stop, arrival, departure in details["stops"]:
            if stop == "Chennai":
                pass

    normal_time = time.time() - start

    # Build index
    start = time.time()
    index = {}

    for number, details in timetable.items():
        for stop, arrival, departure in details["stops"]:
            index.setdefault(stop, []).append(number)

    index_time = time.time() - start

    # Search using index
    start = time.time()
    answer = index.get("Chennai", [])
    fast_time = time.time() - start

    print("\nTrains:", n)
    print("Normal search:", normal_time)
    print("Index creation:", index_time)
    print("Indexed search:", fast_time)

print("Index memory:", sys.getsizeof(station_index))
