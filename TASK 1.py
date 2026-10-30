def subsidy_separate(units, ration_card, elderly_member):
    results = []

    if units <= 100:
        results.append("Full subsidy")

    if 101 <= units <= 200 and ration_card:
        results.append("Partial subsidy")

    if 101 <= units <= 200 and not ration_card:
        results.append("No subsidy")

    if units > 200 and elderly_member:
        results.append("Subsidy under senior-citizen exception")

    if units > 200 and not elderly_member:
        results.append("No subsidy")

    return results


print("Separate if statements:")
print(subsidy_separate(100, True, False))
print(subsidy_separate(101, True, False))
print(subsidy_separate(200, False, False))
print(subsidy_separate(201, True, False))