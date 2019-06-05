import sys

"""
Python file to find words without any similarities from a word list
"""

def usage():
    print("Usage: ./solo_words.py <WORDLIST_PATH>")
    exit()

if len(sys.argv) != 2:
    usage()

file_path = sys.argv[1]

data = []
with open(file_path) as file:
    data = file.readlines()


for line in data:
    parts = line.split(",")

    # Word and newline
    if len(parts) == 2:
        print(line.strip())