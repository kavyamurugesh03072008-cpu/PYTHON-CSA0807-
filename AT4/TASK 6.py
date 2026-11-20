
import os

# Input and output folders
os.makedirs("input", exist_ok=True)
os.makedirs("output/events", exist_ok=True)

# Create sample department files
with open("input/department1.txt", "w") as f:
    f.write(
        "101,Ravi,CSE,ravi@gmail.com,Music;Dance\n"
        "102,Priya,CSE,priya@gmail.com,Singing\n"
    )

with open("input/department2.txt", "w") as f:
    f.write(
        "101,Ravi,CSE,ravi@gmail.com,Drama\n"
        "103,Arun,IT,arun@gmail.com,Music;Drama\n"
    )

with open("input/department3.txt", "w") as f:
    f.write(
        "104,Kumar,EEE,kumar@gmail.com,Dance\n"
        "105,Anu,EEE,invalid-email,Music\n"
    )

with open("input/department4.txt", "w") as f:
    f.write(
        "106,Meena,ECE,meena@gmail.com,Singing\n"
        "107,John,ECE,john@gmail.com\n"
    )

# Department 5 file is intentionally missing


# Validate email
def valid_email(email):
    if " " in email or email.count("@") != 1:
        return False

    username, domain = email.split("@")

    return (
        bool(username)
        and "." in domain
        and not domain.startswith(".")
        and not domain.endswith(".")
    )


# Read and process registrations
def process_registrations(files):

    master = {}
    seen = set()
    errors = []

    for filename in files:

        try:
            with open(filename, "r", encoding="utf-8") as f:

                for line_number, line in enumerate(f, start=1):

                    try:
                        parts = line.strip().split(",", 4)

                        if len(parts) != 5:
                            raise ValueError("Damaged record")

                        reg, name, dept, email, events = parts

                        if not reg or not name or not dept:
                            raise ValueError("Missing required field")

                        if not valid_email(email):
                            raise ValueError("Invalid email")

                        event_list = {
                            event.strip()
                            for event in events.split(";")
                            if event.strip()
                        }

                        if not event_list:
                            raise ValueError("No events selected")

                        # Merge duplicate registrations
                        if reg in seen:
                            master[reg]["events"].update(event_list)
                            master[reg]["emails"].add(email)
                        else:
                            seen.add(reg)

                            master[reg] = {
                                "name": name,
                                "department": dept,
                                "emails": {email},
                                "events": event_list
                            }

                    except ValueError as e:
                        errors.append(
                            f"{filename}, Line {line_number}: {e}"
                        )

        except FileNotFoundError:
            errors.append(f"{filename}: File not found")

        except PermissionError:
            errors.append(f"{filename}: Permission denied")

        except UnicodeDecodeError:
            errors.append(f"{filename}: Encoding error")

    return master, errors


# Write output files
def generate_reports(master, errors):

    # Master list
    with open("output/master_list.txt", "w", encoding="utf-8") as f:

        f.write("COLLEGE FEST MASTER LIST\n\n")

        for reg, details in sorted(master.items()):

            f.write(f"Register Number: {reg}\n")
            f.write(f"Name: {details['name']}\n")
            f.write(f"Department: {details['department']}\n")
            f.write(f"Emails: {', '.join(sorted(details['emails']))}\n")
            f.write(f"Events: {', '.join(sorted(details['events']))}\n")
            f.write("-------------------------\n")

    # Event-wise participant lists
    event_groups = {}

    for reg, details in master.items():

        for event in details["events"]:
            event_groups.setdefault(event, []).append(
                (reg, details["name"])
            )

    for event, participants in event_groups.items():

        safe_name = "".join(
            ch for ch in event if ch.isalnum() or ch in "_-"
        )

        with open(
            f"output/events/{safe_name}.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(f"Participants for {event}\n")

            for reg, name in sorted(participants):
                f.write(f"{reg} - {name}\n")

    # Summary report
    with open("output/summary.txt", "w", encoding="utf-8") as f:

        f.write("COLLEGE FEST SUMMARY\n")
        f.write(f"Total students: {len(master)}\n")
        f.write(f"Total events: {len(event_groups)}\n")

        for event, participants in sorted(event_groups.items()):
            f.write(f"{event}: {len(participants)} participants\n")

    # Error log
    with open("output/error_log.txt", "w", encoding="utf-8") as f:

        for error in errors:
            f.write(error + "\n")


# Main program
files = [
    "input/department1.txt",
    "input/department2.txt",
    "input/department3.txt",
    "input/department4.txt",
    "input/department5.txt"
]

master, errors = process_registrations(files)

generate_reports(master, errors)

print("College fest processing completed.")
print("Total students:", len(master))
print("Total errors:", len(errors))
print("Master list created.")
print("Event-wise files created.")
print("Summary report created.")
print("Error log created.")
