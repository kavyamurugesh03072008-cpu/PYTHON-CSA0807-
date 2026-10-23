import math

# Constants
BASE_RATE = 30.0
BASE_FAT = 3.5
BASE_SNF = 8.5
FAT_RATE = 0.40
SNF_RATE = 0.30

# Get input 
fat= float(input("Enter the fat percentage: "))
snf= float(input("Enter the SNF percentage: "))
liters= float(input("Enter the number of liters: "))

#calculate fat and snf steps
fat_steps = round((fat - BASE_FAT) / 0.1)
snf_steps = round((snf - BASE_SNF) / 0.1)

print("Fat steps:", fat_steps)
print("SNF steps:", snf_steps)

#calculate rate per liter
rate = BASE_RATE + (fat_steps * FAT_RATE) + (snf_steps * SNF_RATE)
print("Rate per liter:", rate)

#calculate total amount
amount = rate * liters
print("Total amount: Rs", round(amount, 2))

#Demonstrate unexpected results
print("\nUNEXPECTED RESULTS")
print("(4.2-3.5)/0.1 = ", (4.2-3.5)/0.1)
print("0.1+0.2=", 0.1+0.2)
print("0.1+0.2==0.3?", 0.1+0.2==0.3)

# Compare round(), int(), and math.floor()
print("\nSTEP COUNT COMPARISON")
for fat_value in [4.2, 3.1]:
    steps = (fat_value - BASE_FAT) / 0.1
    print("Fat:", fat_value)
    print("Exact calculation:", steps)
    print("round():", round(steps))
    print("int():", int(steps))
    print("math.floor():", math.floor(steps))

    # Operator precedence
    print("\nOPERATOR PRECEDENCE")
    print("2**3**2 =", 2**3**2)
    print("-2**2 =", -2**2)
    print("(-2)**2 =", (-2)**2)

    # Comparison chaining and Boolean operators
    print("\nVALIDATION")
    print("Fat valid:", 2.0<=fat <=7.0)
    print("SNF valid:", 6.0<=snf <=10.0)
    print("Both vaild:", 2.0<=fat <=7.0 and 6.0<=snf <=10.0)

    #complexity
    print("\nTIME COMPLEXITY: O(1)")
    print("SPACE COMPLEXITY: O(1)")