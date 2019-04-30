import sys

"""
Script that converts provided argument into
base 2 complexity notation

i.e 16 = 2^4
"""

def usage():
    print("[!] Usage: python base_2.py <VALUE>")
    exit(0)

# Checks for correct number of arguments
if len(sys.argv) != 2:
    usage()

# Performs the argument parse
try:
    number = int(sys.argv[1])
except ValueError:
    print("[!] Error - value isn't numerical\n")
    usage()

intermediate = number
counter = 0

while intermediate > 1:
    intermediate /= 2
    counter += 1

print(f"[*] 2^{counter}")

