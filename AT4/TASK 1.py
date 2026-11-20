
# TASK 1: Hostel Mess Bill Processing

def process_file(filename):
    total = 0.0
    report = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as f:

            for line_number, line in enumerate(f, start=1):
                if not line.strip():
                    continue

                try:
                    parts = line.strip().split(",")

                    if len(parts) != 3:
                        raise ValueError("Incorrect number of fields")

                    register_no = parts[0].strip()
                    name = parts[1].strip()
                    amount = float(parts[2].strip())

                    total += amount
                    report.append(f"{name} - Rs.{amount:.2f}")

                except ValueError as e:
                    rejected.append((line_number, line.strip(), str(e)))

        print("MESS BILL REPORT")
        for item in report:
            print(item)

        print("Total Mess Bill: Rs.", format(total, ".2f"))

        print("\nRejected Records:")
        for item in rejected:
            print(item)

    except FileNotFoundError:
        print("Error: File not found.")

    except PermissionError:
        print("Error: Permission denied.")

# Sample file creation
sample_data = """192311001,Ravi,1250.50
192311002,Priya,1500.00
192311003,Arun,1200.75
192311004,Kumar,invalid
"""

with open("mess_oct.txt", "w", encoding="utf-8") as f:
    f.write(sample_data)

process_file("mess_oct.txt")
