
import os
import tempfile

# Original program with defects
def save_returns(books):
    log = open("returns.log", "w")

    for book in books:
        log.write(book)

    log.close()


def process(day_file):
    try:
        books = open(day_file).read().split("\n")
        save_returns(books)

    except FileNotFoundError:
        print("Missing file")


# Create sample daily files
daily_files = ["day1.txt", "day2.txt", "day3.txt"]

data = [
    "Book A\nBook B",
    "Book C\nBook D",
    "Book E\nBook F"
]

for filename, content in zip(daily_files, data):
    with open(filename, "w") as f:
        f.write(content)

# Demonstrate original defects
print("Original program:")

for filename in daily_files:
    process(filename)

with open("returns.log", "r") as f:
    print("Log contents:", repr(f.read()))


# Corrected program
def save_returns(books):
    with open("returns.log", "a", encoding="utf-8") as log:
        for book in books:
            if book.strip():
                log.write(book + "\n")


def process_corrected(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as f:
            books = f.read().splitlines()

        save_returns(books)

    except FileNotFoundError as e:
        with open("error.log", "a", encoding="utf-8") as log:
            log.write(str(e) + "\n")

    except PermissionError as e:
        with open("error.log", "a", encoding="utf-8") as log:
            log.write(str(e) + "\n")


# Remove old log
if os.path.exists("returns.log"):
    os.remove("returns.log")

# Run corrected program
print("\nCorrected program:")

for filename in daily_files:
    process_corrected(filename)

with open("returns.log", "r", encoding="utf-8") as f:
    print(f.read())

print("All daily returns saved successfully.")
