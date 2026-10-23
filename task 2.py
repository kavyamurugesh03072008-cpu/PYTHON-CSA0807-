from decimal import Decimal
import sys

#explore data types
print("DATA TYPES")
print(type(10))
print(type(10.0))
print(type("10"))
print(type(True))
print(type([10,8.5]))

#Division operators
print("\nDIVISION OPERATORS")
print("7/2=", 7/2)
print("7//2=", 7//2)
print("7%2=", 7%2)
print("7.0/2.0=", 7.0/2.0)

#Floting point problems
print("\nFLOATING POINT PROBLEMS")
print("0.1 + 0.2=", 0.1 + 0.2)
print("Float equality:", 0.1 + 0.2 == 0.3)
print("Decimal equality:", Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))

#payment data
payments = ["33.40"]*1000 + ["0.10"]*3

#calcuate total using float
def total_float(items):
    total = 0.0
    for amount in items:
      total += float(amount)
    return total

#calcuate total using decimal
def total_decimal(items):   
    total = Decimal('0.0')
    for amount in items:
      total += Decimal(amount)
    return total

#calculate total using integer paise
def total_paise(items):
    total = 0
    for amount in items:
      rupees, paise = amount.split(".")
      total += int(rupees) * 100 + int(paise)
    return total

#calculate total using round()
def total_round(items):
    total = 0.0
    for amount in items:
      total += round(float(amount), 2)
    return total

#display totals
print("\nPAYMENT TOTALS")
print("Float:", total_float(payments))
print("Decimal:", total_decimal(payments))
print("Paise:", total_paise(payments))
print("Rounded float:", total_round(payments))

#Memory comparison
print("\nMEMORY COMPARISON")
print("Float:", sys.getsizeof(33.40))
print("Decimal:", sys.getsizeof(Decimal('33.40')))
print("Paise:", sys.getsizeof(3340))

