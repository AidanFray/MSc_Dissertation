import sys
import random

"""
Script that is used to generate a number of random pairs from
a "similar word" list
"""


def usage():
    print(f"[!] Usage: ./{__file__} <SIMILAR_LIST> <NUM_OF_PAIRS>")
    exit()

def remove_matchless_words(similar_list):
    """
    Removes any words without any matches
    """

    new_list = []
    for sword in similar_list:

        parts = sword.split(",")

        if len(parts) > 2:
            new_list.append(sword)

    return new_list

def spread_out_matches(similar_list):

    new_list = []
    for sword in similar_list:

        sword = sword.strip()
        parts = sword[:-1].split(",")

        for p in parts[1:]:
            new_list.append(f"{parts[0]},{p}")

    return new_list

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        usage()

    similar_list_path = sys.argv[1]
    num_of_pairs = int(sys.argv[2])

    similar_list = []
    with open(similar_list_path) as f:
        similar_list = f.readlines()

    similar_list = remove_matchless_words(similar_list)
    similar_list = spread_out_matches(similar_list)

    # Prints out the random pairs
    for n in range(num_of_pairs):
        index = random.randint(0, len(similar_list))
        print(similar_list[index])