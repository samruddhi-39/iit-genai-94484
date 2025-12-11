
#Q1:
# Write a Python program that takes a sentence from the user and prints:
# Number of characters
# Number of words
# Number of vowels
# Hint: Use split(), loops, and vowel checking.
sent = input("Enter a sentence: ")
charac = len(sent.replace(" ", ""))
words = len(sent.split())
vowels = "aeiouAEIOU"
vowel_count = 0
for char in sent:
    if char in vowels:
        vowel_count += 1

print("\n--- Output ---")
print("Number of characters:", charac)
print("Number of words:", words)
print("Number of vowels:", vowel_count)

