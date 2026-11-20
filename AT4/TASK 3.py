
import os
import tempfile

class InvalidRecord(Exception):
    """Invalid attendance record exception."""

def parse_line(line):
    parts = line.strip().split(",")

    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )

    if parts[2] not in ("P", "A"):
        raise InvalidRecord(
            f"invalid status '{parts[2]}'"
        )

    return tuple(part.strip() for part in parts)

def summarise(path):
    present, absent, errors = 0, 0, []

    try:
        with open(path, "r", encoding="utf-8") as f:

            for line_number, line in enumerate(f, start=1):
                try:
                    reg_no, date, status = parse_line(line)

                    if status == "P":
                        present += 1
                    else:
                        absent += 1

                except InvalidRecord as e:
                    errors.append((line_number, str(e)))

        return present, absent, errors

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Attendance file not found: {path}"
        ) from e

    except PermissionError as e:
        raise PermissionError(
            f"Permission denied: {path}"
        ) from e

    except UnicodeDecodeError as e:
        raise UnicodeError(
            f"Invalid file encoding: {path}"
        ) from e

    finally:
        print("File processing completed.")

# Sample data
data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

with tempfile.NamedTemporaryFile(
    "w", suffix=".csv", delete=False, encoding="utf-8"
) as tmp:
    tmp.write(data)
    filename = tmp.name

try:
    print(summarise(filename))

except (FileNotFoundError, PermissionError, UnicodeError) as e:
    print("Error:", e)

finally:
    os.remove(filename)

# Test missing file
try:
    summarise("unknown_file.csv")

except FileNotFoundError as e:
    print("Handled:", e)
