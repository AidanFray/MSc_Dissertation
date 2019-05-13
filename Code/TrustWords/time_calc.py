import sys

"""
Small script used to calculate time needed to compute collisions of TrustWords
"""

def usage():
    print("[!] python time_calc.py <LENGTH_IN_CHARS> <PERMUTATIONS>")
    exit()

if len(sys.argv) != 3:
    usage()

HASHSPEED = 2700000000

length_in_chars = float(sys.argv[1])
permutations = float(sys.argv[2])

time_seconds = 2**(4*length_in_chars-1) / HASHSPEED / permutations

time_days = time_seconds / 3600 / 24

print(f"[*] It will take {round(time_days, 2)} days!")
print(f"[*] It will take {round(time_days / 365, 2)} years!")
