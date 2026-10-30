correct_otp = "1234"
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    otp = input("Enter OTP: ")

    if otp == "":
        print("Blank entry! Please enter the OTP.")
        continue

    attempts += 1

    if otp == correct_otp:
        print("OTP verified successfully!")
        break
    else:
        print("Wrong OTP. Attempts used:", attempts)

    if attempts < max_attempts:
        pass  # Placeholder for additional processing

else:
    print("Account locked for 30 minutes.")