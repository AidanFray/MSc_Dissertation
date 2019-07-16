import sys 
import os

sys.path.insert(0, "..")

from util.trustwords import *
from util.permutations import *
from util.timing import *
from util.CONFIG import HASHSPEED

def create_random_fingerprint(number_of_words):
    return os.urandom(8).hex()

def determine_average_perms(number_of_words, mapping, all_perms=True):

    max_perm = 0
    min_perm = None
    loops = 1000000

    total_all = 0
    total_one_static = 0
    total_two_static = 0

    for _ in range(loops):
        fingerprint = create_random_fingerprint(number_of_words)

        trustwords = fingerprint_to_words(fingerprint, mapping, PRINT=False)

        if all_perms:
            combinations = similar_combinations(trustwords, mapping)

            one_static_combinatsions = similar_combinations(trustwords, mapping, staticPos=[0])
            two_static_combinatsions = similar_combinations(trustwords, mapping, staticPos=[0, 3])

            perm_len = get_perm_size(combinations)

            # # UNCOMMENT TO Print values out to file
            # print(str(perm_len) + ",")

            one_perm_len = get_perm_size(one_static_combinatsions)
            two_perm_len = get_perm_size(two_static_combinatsions)
        else:
            combinations = multimap_combinations(trustwords, mapping)
            perm_len = get_perm_size(combinations)
        
        # MAX
        if perm_len > max_perm:
            max_perm = perm_len

        # MIN
        if min_perm == None or perm_len < min_perm:
            min_perm = perm_len

        total_all += perm_len
        total_one_static += one_perm_len
        total_two_static += two_perm_len

    average_all_perm = total_all / loops
    average_static_one_perm = total_one_static / loops
    average_static_two_perm = total_two_static / loops

    # 4 hex chars per word
    number_of_characters = float(number_of_words * 4)

    min_time = calculate_runtime(number_of_characters, min_perm)
    max_time = calculate_runtime(number_of_characters, max_perm)

    average_all_time = calculate_runtime(number_of_characters, average_all_perm)
    average_one_static = calculate_runtime(number_of_characters,average_static_one_perm)
    average_two_static = calculate_runtime(number_of_characters,average_static_two_perm)

    print(f"[!] At a speed of {HASHSPEED}MH/s")
    print(f"[!] Average permutations is: {average_all_perm}")
    print_timing(average_all_time)

    print(f"[!] Average one static word permutations is: {average_static_one_perm}")
    print_timing(average_one_static)

    print(f"[!] Average two static word permutations is: {average_static_two_perm}")
    print_timing(average_two_static)

    print(f"[!] Max: {max_perm}")
    print_timing(max_time)

    print(f"[!] Min: {min_perm}")
    print_timing(min_time)
    