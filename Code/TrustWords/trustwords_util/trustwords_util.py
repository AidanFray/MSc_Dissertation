import re
import os
import base64
import argparse
import itertools
from pretty_bad_protocol import gnupg

from util.permutations import *
from util.trustwords import *

from util.timing import calculate_runtime, print_timing
from util.CONFIG import HASHSPEED

from mappings import Mappings

# MODES
import modes.vuln_keys as VK
import modes.average_perms as AP
import modes.words_from_keys as WK
import modes.create_actual_key as CK
import modes.perms_from_words as PW

file_path = "."

# GPG object
gpg = gnupg.GPG(options=["--debug-quick-random"])

# Object that contains all the mapping dictionaries
mapping = Mappings()

def load_mappings(fileName):
    """
    Loads the hex -> word mapping into a local dictionary
    """

    with open(f"{file_path}/{fileName}") as file:

        line = None
        while True:
            line = file.readline()
            if line == '':
                break
            
            line_parts = line.split(",")

            # Maps string to
            word = line_parts[2]
            word_hex = hex(int(line_parts[1]))[2:].zfill(4)

            # Hex --> Word
            mapping._hex_to_word_mapping.update(
                {
                    word_hex: word
                })

            # Word --> Hex
            if word in mapping._word_to_hex_mapping:
                mapping._word_to_hex_mapping[word].append(word_hex)
            else:
                mapping._word_to_hex_mapping.update({word: [word_hex]})

def load_similar_mappings(fileName):
    """
    Loads the mapping that have been found to be similar
    from an external file. The external loading uncouples
    this program from the method used to determine
    'similarity'
    """
    with open(f"{file_path}/{fileName}") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        line_parts = line.split(",")

        base_word = line_parts[0]
        similar_words = line_parts[1:-1]

        mapping._similar_word_mapping.update({base_word: similar_words})

def save_permutations(perms, outFileName):
    """
    Saves the potential key permutations to file
    """

    with open(f"./{outFileName}", "w") as file:
        for p in perms:
            file.write(p.lower())
            file.write("\n")

def find_possible_keys(perms, uncontrolledFingerprint):
    """
    This method is used to produce a list of key fingerprints that would be near
    matches to the valid fingerprints
    """

    key_possibilities = []
    for p in perms:

        possible_fingerprint = "".join(p)

        f = XOR_fingerprints(possible_fingerprint, uncontrolledFingerprint)

        key_possibilities.append(f)

    return key_possibilities

def load_key_from_file_and_return_fingerprint(filePath, number_of_words):

    data = None
    with open(filePath) as file:
        data = file.read()

    import_result = gpg.import_keys(data)

    fingerprint = import_result.fingerprints[0]
    print(fingerprint)

    formatted_fingerprint = []
    for x in range(0, len(fingerprint), 4):
        formatted_fingerprint.append(fingerprint[x:x+4])

    return " ".join(formatted_fingerprint[-number_of_words:])

def args():
    # The fingerprint of the target
    UNCONTROLLED_FINGERPRINT    = "7E6C 4BF0 5CF3 F379"
    # UNCONTROLLED_FINGERPRINT    = "7E6C 4BF0 5CF3 F379 1191"

    # The fingerprint we can change via MITM
    CONTROLLABLE_FINGERPRINT    = "2F88 CE86 1A1B 19D3"
    # CONTROLLABLE_FINGERPRINT    = "2F88 CE86 1A1B 19D3 5F80"

    parser = argparse.ArgumentParser(description='Compute similar TrustWord keys')

    # Modes
    parser.add_argument("-m","--multi-mappings", dest="multi", action="store_true")
    parser.add_argument("--am", "--average-multi", dest="average_multi", action="store_true")
    parser.add_argument("-a", "--average", dest="average", action="store_true")
    parser.add_argument("-t", "--trustwords", dest="trustwords", nargs=2, action="store")
    parser.add_argument("-f", "--find-keys", dest="find_keys", action="store_true")
    
    # Params
    parser.add_argument("-k", "--key", dest="key", nargs=1, action="store")
    parser.add_argument("-s", "--similar-wordlist", dest="similar", nargs=1, action="store")
    parser.add_argument("-l", "--langauge", dest="lang", nargs=1, action="store")
    parser.add_argument("-n","--num-of-words", dest="num_words", nargs=1, type=int, action="store")
    parser.add_argument("-o", "--output-file-name", dest="output", nargs=1, action="store")
    parser.add_argument("-p", "--perms-for-words", dest="perms", nargs=1, action="store")
    parser.add_argument("--vuln-keys", dest="vuln", nargs=2, action="store")
    
    arg = parser.parse_args()

    # Number of words
    number_of_words = arg.num_words[0] if arg.num_words else 4

    # Output file name
    outFileName = arg.output[0] if arg.output else "target_keys.txt"

    if arg.key:
        CONTROLALBLE_FINGERPRINT = load_key_from_file_and_return_fingerprint(arg.key[0], number_of_words)

    # Loads the file paths for similar wordlist
    if arg.similar: 
        similar_mappings_file_name = arg.similar[0]
        load_similar_mappings(similar_mappings_file_name)

    # Sets the dictionary mapping file - Default is english
    dictionary_file_name = f"../../../Wordlists/Trustwords/{args.lang[0].upper()}/{args.lang[0].lower()}.csv" \
        if arg.lang else f"../../../Wordlists/Trustwords/EN/en.csv"
    load_mappings(dictionary_file_name)

    ### MODES ###
    # Average number of potential keys
    if arg.average:
        AP. determine_average_perms(number_of_words, mapping)
        exit()

    # Finds number of average multi mapping perms
    if arg.average_multi:
        AP. determine_average_perms(number_of_words, mapping, all_perms=False)
        exit()

    # Outputs the trust words for two actual keys
    if arg.trustwords:
        WK.generate_words_for_PGP_keys(arg.trustwords[0], arg.trustwords[1], mapping)
        exit()

    # Finds an actual key that produces the higest permutation size
    if arg.find_keys:
        CK.create_actual_fingerprint_and_key(number_of_words, UNCONTROLLED_FINGERPRINT, mapping, gpg)
        exit()

    # Returns the number of permutations for a trustword set
    if arg.perms:
        PW.num_of_perms_of_words(arg.perms[0], mapping)
        exit()

    # Form an key list argument this code returns a list of keys that have
    # more permuatations that the specificed number
    if arg.vuln:
        key_list_path = arg.vuln[0]
        num_of_perms = int(arg.vuln[1])

        VK.find_vuln_keys(key_list_path, mapping, num_of_perms)    
        exit()

    combined_fingerprint = XOR_fingerprints(CONTROLLABLE_FINGERPRINT, UNCONTROLLED_FINGERPRINT)
    trustwords = fingerprint_to_words(combined_fingerprint, mapping)

    # Creates list of multiple mapping
    # i.e. the word "TREE" maps to 0xff43 and 0xf3ee
    if arg.multi:
        perms = multimap_perms(trustwords, mapping) 
        key_possibilities = find_possible_keys(perms, UNCONTROLLED_FINGERPRINT)
        save_permutations(key_possibilities, outFileName)

    # Default mode of finding all mappings
    else:
        perms = similar_perms(trustwords, mapping)

        key_possibilities = find_possible_keys(perms, UNCONTROLLED_FINGERPRINT)
        save_permutations(key_possibilities, outFileName)

if __name__ == "__main__":
    args()