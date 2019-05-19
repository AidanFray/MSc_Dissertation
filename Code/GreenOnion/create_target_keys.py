import sys

"""
A script to create a dud target_keys file.
This is used to calculate speed required
"""

def usage():
    print("[!] python create_target_keys.py <NUMBER_OF_KEYS>")
    exit()

if len(sys.argv) != 2:
    usage()

number_of_keys = int(sys.argv[1])

# Starts off at 0 and just increments up
data = 0

with open("target_keys.txt", "w") as file:
    for x in range(number_of_keys):
        data_str = str(hex(data)[2:]).zfill(16)
        file.write(data_str + "\n")
        data += 1

print("[+] Save complete!")