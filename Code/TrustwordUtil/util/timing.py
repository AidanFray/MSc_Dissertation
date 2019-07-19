from .CONFIG import *

def calculate_runtime(length_in_chars, permutations):
    length_in_chars = float(length_in_chars)
    hashspeed = int(HASHSPEED * 1000000)
    permutations = float(permutations)

    top = (2**(4 * (length_in_chars)))
    time_seconds = top / hashspeed / permutations
   
    return time_seconds


def print_timing(time_seconds):

    time_days = time_seconds / 3600 / 24
    print()
    print(f"        {round(time_seconds, 2)} seconds!")
    print(f"        {round(time_seconds / 60, 2)} minutes!")
    print(f"        {round(time_days, 2)} days!")
    print(f"        {round(time_days / 365, 2)} years!")
    print()
