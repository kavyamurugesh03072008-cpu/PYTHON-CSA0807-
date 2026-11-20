
# attendance.py

def read_data():
    return [("101", 80), ("102", 60), ("103", 90)]


def calculate_percentage(data):
    return {reg: percentage for reg, percentage in data}


def write_report(result):
    with open("report.txt", "w") as f:
        for reg, percentage in result.items():
            f.write(f"{reg}: {percentage}%\n")


def consecutive_absentees(data):
    # Sample consecutive absence report
    return ["102"]


def main():
    data = read_data()
    result = calculate_percentage(data)
    write_report(result)

    print("Attendance:", result)
    print("Three-day absent students:",
          consecutive_absentees(data))


if __name__ == "__main__":
    main()
