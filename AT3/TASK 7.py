
import time
import random

# Sample contacts from different phones
contacts = [
    {
        "name": "Dr. Ravi",
        "phone": "+91 98400 12345",
        "email": "ravi@gmail.com"
    },
    {
        "name": "Ravi Kumar",
        "phone": "9840012345",
        "email": "ravi@gmail.com"
    },
    {
        "name": "Priya",
        "phone": "9876543210",
        "email": "priya@gmail.com"
    },
    {
        "name": "Priya S",
        "phone": "+91-98765-43210",
        "email": "priya@yahoo.com"
    },
    {
        "name": "Arun",
        "phone": "",
        "email": "arun@gmail.com"
    }
]

# Normalize phone number
def normalize_phone(phone):
    return "".join(ch for ch in phone if ch.isdigit())

# Normalize name
def normalize_name(name):
    return " ".join(name.lower().strip().split())

# Merge contacts
def merge_contacts(contact_list):
    merged = {}

    for contact in contact_list:
        phone = normalize_phone(contact["phone"])
        name = normalize_name(contact["name"])
        email = contact["email"].lower().strip()

        # Use phone as the main key
        key = phone if phone else "no_phone_" + name

        if key not in merged:
            merged[key] = {
                "names": set(),
                "phones": set(),
                "emails": set()
            }

        merged[key]["names"].add(contact["name"])

        if phone:
            merged[key]["phones"].add(phone)

        if email:
            merged[key]["emails"].add(email)

    return merged

# Display merged contacts
result = merge_contacts(contacts)

print("Merged Contacts")

for key, details in result.items():
    print("\nNames:", sorted(details["names"]))
    print("Phone numbers:", sorted(details["phones"]))
    print("Emails:", sorted(details["emails"]))

# Test missing fields
test_contacts = [
    {"name": "Anu", "phone": "", "email": ""},
    {"name": "Anu", "phone": "", "email": ""}
]

print("\nMissing field test:")
print(merge_contacts(test_contacts))

# Compare with pairwise comparison
def pairwise_merge(data):
    groups = []

    for contact in data:
        phone = normalize_phone(contact["phone"])
        found = False

        for group in groups:
            if phone and phone in group["phones"]:
                group["names"].add(contact["name"])
                if contact["email"]:
                    group["emails"].add(contact["email"])
                found = True
                break

        if not found:
            groups.append({
                "names": {contact["name"]},
                "phones": {phone} if phone else set(),
                "emails": {contact["email"]} if contact["email"] else set()
            })

    return groups

# Generate large contact datasets
for n in [1000, 100000]:

    data = []

    for i in range(n):
        number = str(9000000000 + random.randint(0, n - 1))

        data.append({
            "name": "Person " + str(i),
            "phone": number,
            "email": "person" + str(i) + "@gmail.com"
        })

    # Dictionary method
    start = time.time()
    merged = merge_contacts(data)
    dictionary_time = time.time() - start

    print("\nContacts:", n)
    print("Dictionary merging time:", dictionary_time)

    # Pairwise method on a smaller sample
    if n == 1000:
        start = time.time()
        groups = pairwise_merge(data)
        pairwise_time = time.time() - start

        print("Pairwise merging time:", pairwise_time)
