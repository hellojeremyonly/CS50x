from cs50 import get_float

# Constants representing coin values in cents
QUARTER = 25
DIME = 10
NICKEL = 5
PENNY = 1

# Prompt the user for the amount of change owed
while True:
    try:
        dollars = get_float("Change owed: ")
        if dollars > 0:
            break
        else:
            print("Invalid input")
    except:
        print("Invalid input. Please enter a number.")

# Convert dollars to cents
cents = round(dollars * 100)

# Calculate the minimum number of coins
coins = 0
coins += cents // QUARTER
cents %= QUARTER
coins += cents // DIME
cents %= DIME
coins += cents // NICKEL
cents %= NICKEL
coins += cents // PENNY

# Print the minimum number of coins
print(coins)
