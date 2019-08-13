import sys

"""
Python script to output unique words form a TrustWord dictionary
"""

def usage():
    print("Usage: python unique_wordlist.py <WORDLIST>")
    exit()

if len(sys.argv) != 2:
    usage()

in_filepath = sys.argv[1]

# Removes .csv and adds "_unique.csv"
out_filepath = in_filepath.split('.')[0] + "_unique.csv"

lines = []
with open(in_filepath) as file:
    lines = file.readlines()

# Loop though lines and add unique words
words = {} 
for line in lines:
    line_parts = line.split(",")

    word = line_parts[2]

    if not word in words:
        words.update({word : ""})

# Save unique words to file
with open(out_filepath, "w") as file:
    for word in words:
        file.write(word)
        file.write("\n")

print("[*] Unique words saved!")