BASE_RATE = 30.0
BASE_FAT = 3.5
BASE_SNF = 8.5
FAT_RATE = 0.40
SNF_RATE = 0.30

def rate_per_litre(fat, snf):
    """Calculate and return the milk rate per liter"""
    fat_steps = round((fat - BASE_FAT) / 0.1)
    snf_steps = round((snf - BASE_SNF) / 0.1)
    rate = BASE_RATE + (fat_steps * FAT_RATE) + (snf_steps * SNF_RATE)
    return rate

def payout(liters,rate):
    """Calculate and return the total payout for the given liters and rate"""
    amount = liters * rate
    return round(amount, 2)

def ten_day_total(daily_payments):
    """Calculate and return the total payout for 10 days"""
    return round(sum(daily_payments), 2)

def main():
    """ Read milk details, calculate the rate and display the bill"""
    try:
        fat = float(input("Enter fat percentage: "))
        snf = float(input("Enter SNF percentage: "))
        liters = float(input("Enter liters of milk: "))

    if liters < 0:
        print("Liters must be greater than zero.")
        return

    rate = rate_per_litre(fat, snf)
    amount = payout(liters, rate)

    print("\n -- Milk Bill --")
    print(f"Fat Percentage: {fat}%")
    print(f"SNF Percentage: {snf}%")
    print(f"Liters of Milk: {liters} L")
    print(f"Rate per Liter: ${rate:.2f}")
    print(f"Total Amount: ${amount:.2f}")

    #example of calculating 10-day total
    daily_payments = [amount] * 10 
    print(f"\nTotal Payout for 10 Days: ${ten_day_total(daily_payments):.2f}")
    except ValueError:
        print("Invalid input. Please enter numeric values for fat, SNF, and liters.")  

    if __name__ == "__main__":
        main() 
    