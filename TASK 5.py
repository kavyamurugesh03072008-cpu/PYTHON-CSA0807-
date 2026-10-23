while True:
    fat_text = input("Enter fat percentage:").strip()
    try:
        fat = float(fat_text)
        break
    except ValueError:
        print("Invalid input! Enter a number, for example 4.2.")

# validate SNF percentage
while True:
    snf_text = input("Enter SNF percentage:").strip()
    try:
        snf = float(snf_text)
        break
    except ValueError:
        print("Invalid input! Enter a number, for example 8.5.")
        try:
            snf = float(snf_text)
            break
        except ValueError:
            print("Invalid input! Enter a number, for example 8.5.")    
# validate liters
while True:
    liters_text = input("Enter liters:").strip()
    try:
        liters = float(liters_text)
        if liters <= 0:
            print("Liters must be greater than 0.")
            continue
        break
    except ValueError:
        print("Invalid input! Enter a number, for example 10.")

# Calculate amount
BASE_RATE = 30.0
BASE_FAT = 3.5
BASE_SNF = 8.5
FAT_RATE = 0.40
SNF_RATE = 0.20

fat_steps = round((fat - BASE_FAT) / 0.1)
snf_steps = round((snf - BASE_SNF) / 0.1)   

rate = BASE_RATE + (fat_steps * FAT_RATE) + (snf_steps * SNF_RATE)
amount = rate * liters

# results
print("\n------MILK BILL ------")
print(f"Fat: {fat}%")
print(f"SNF: {snf}%")
print(f"Liters: {liters}")
print(f"Rate: {rate:.2f}")
print(f"Amount: {amount:.2f}")