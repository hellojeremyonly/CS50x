# Prompt the user for the half-pyramid's height
while True:
    height = int(input("Height: "))
    if 1 <= height <= 8:
        break

# Generate pyramid
for i in range(height):
    # Print spaces for the first half
    for j in range(height - i - 1):
        print(" ", end="")
    # Print hashes for the first half
    for j in range(i + 1):
        print("#", end="")
    # Print a new line
    print()
