#Task 1
from decimal import Decimal,ROUND_HALF_UP
#Constants
base_rate=Decimal("30.00")
base_fat=Decimal("3.5")
base_snf=Decimal("8.5")

fat_rate=Decimal("0.40")
snf_rate=Decimal("0.30")

#function of calculating milk price
def milk_price(fat,snf):
    fat_change = (fat - base_fat)/Decimal("0.1")
    snf_change = (snf - base_snf)/Decimal("0.1")
    rate= base_rate + (fat_change * fat_rate)
    rate=rate + (snf_change * snf_rate)
    return rate

#get input from user
farmer_id=input("Enter farmer ID: ")
liters=input("Enter liters of milk: ")
fat=input("Enter fat percentage: ")
snf=input("Enter SNF percentage: ")

#calculate rate and payment
rate= milk_price(fat,snf)

amount=(liters*rate).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
#Display results
print("\n---Milk Payment Details---")
print("Farmer ID:",farmer_id)   
print("Rate per liter: Rs.", rate)
print("Total payment: Rs.", amount)
