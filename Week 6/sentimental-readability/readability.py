from cs50 import get_string
import re

# Prompt the user for the text
text = get_string("Text: ")

# Count the number of letters, words, and sentences
letters = len(re.findall(r'[a-zA-Z]', text))
words = len(re.findall(r'\b\w+\b', text))
sentences = len(re.findall(r'[.!?]', text))

# Calculate the Coleman-Liau index
L = letters / words * 100
S = sentences / words * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

# Print the grade level
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
