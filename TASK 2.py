
import os

def process_attendance(folder):
    attendance = {}
    errors = []

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)

            try:
                with open(path, "r", encoding="utf-8") as f:

                    for line_number, line in enumerate(f, start=1):
                        try:
                            parts = line.strip().split(",")

                            if len(parts) != 3:
                                raise ValueError("Invalid fields")

                            reg_no, date, status = parts

                            if status not in ("P", "A"):
                                raise ValueError("Invalid status")

                            if reg_no not in attendance:
                                attendance[reg_no] = [0, 0]

                            if status == "P":
                                attendance[reg_no][0] += 1
                            else:
                                attendance[reg_no][1] += 1

                        except ValueError as e:
                            errors.append(
                                (filename, line_number, str(e))
                            )

            except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
                errors.append((filename, 0, str(e)))

    with open("attendance_report.txt", "w", encoding="utf-8") as f:
        f.write("Attendance Report\n")

        for reg_no, counts in attendance.items():
            present, absent = counts
            total = present + absent
            percentage = present / total * 100

            f.write(
                f"{reg_no}: {percentage:.2f}%\n"
            )

    with open("below_75.txt", "w", encoding="utf-8") as f:
        for reg_no, counts in attendance.items():
            present, absent = counts
            total = present + absent
            percentage = present / total * 100

            if percentage < 75:
                f.write(reg_no + "\n")

    with open("attendance_errors.txt", "w", encoding="utf-8") as f:
        for error in errors:
            f.write(str(error) + "\n")

    print("Attendance processing completed.")
    print("Report files created.")

# Create sample folder and files
os.makedirs("attendance", exist_ok=True)

with open("attendance/day1.txt", "w", encoding="utf-8") as f:
    f.write(
        "192311001,2026-10-01,P\n"
        "192311002,2026-10-01,A\n"
        "192311003,2026-10-01,L\n"
    )

with open("attendance/day2.txt", "w", encoding="utf-8") as f:
    f.write(
        "192311001,2026-10-02,P\n"
        "192311002,2026-10-02,P\n"
    )

process_attendance("attendance")
