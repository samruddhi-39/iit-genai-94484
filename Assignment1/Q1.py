# Q1:
# Write a Python program that takes a sentence from the user and prints:

# Number of characters

# Number of words

# Number of vowels

# Hint: Use split(), loops, and vowel checking.

sentence = input("Enter a sentence: ")

# Number of characters (excluding spaces)
characters = len(sentence.replace(" ", ""))

# Number of words
words = len(sentence.split())

# Number of vowels
vowels = "aeiouAEIOU"
vowel_count = 0
for char in sentence:
    if char in vowels:
        vowel_count += 1

print("\n--- Output ---")
print("Number of characters:", characters)
print("Number of words:", words)
print("Number of vowels:", vowel_count)
