import re
import os
import base64
import argparse
import itertools
from pretty_bad_protocol import gnupg

from Crypto.Hash import SHA1
from permutations import *

from timing import calculate_runtime, print_timing
from CONFIG import HASHSPEED

file_path = "."

# GPG object
gpg = gnupg.GPG(options=["--debug-quick-random"])

# Stops the program from generating permutations that fill the RAM

hex_to_word_mapping = {}
word_to_hex_mapping = {}
similar_word_mapping = {} 

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
            hex_to_word_mapping.update(
                {
                    word_hex: word
                })

            # Word --> Hex
            if word in word_to_hex_mapping:
                word_to_hex_mapping[word].append(word_hex)
            else:
                word_to_hex_mapping.update({word: [word_hex]})

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

        similar_word_mapping.update({base_word: similar_words})

def save_permutations(perms, outFileName):
    """
    Saves the potential key permutations to file
    """

    with open(f"./{outFileName}", "w") as file:
        for p in perms:
            file.write(p.lower())
            file.write("\n")

def fingerprint_to_words(fingerprint, PRINT=True):
    """
    Maps the hex value of the key to a word defined in
    the dictionary loaded
    """

    fingerprint = fingerprint.replace(" ", "")

    trustwords = []

    chunks = re.findall(".{4}", fingerprint)

    for chunk in chunks:
        word = hex_to_word_mapping[chunk.lower()]
        trustwords.append(word)

    if PRINT:

        trustwords_str = " ".join(trustwords)

        print("#" * (len(trustwords_str) + 1))
        print(trustwords_str)
        print("#" * (len(trustwords_str) + 1))

    return trustwords

def XOR_fingerprints(fingerprint1, fingerprint2):
    """
    XORs two fingerprints, this is usefull because pEp
    creates a joint fingerprint from the two parties
    by XORing each parties key
    """

    fingerprint1 = fingerprint1.replace(" ", "")
    fingerprint2 = fingerprint2.replace(" ", "")

    fingerprint_1_parts = re.findall(r".{4}", fingerprint1)
    fingerprint_2_parts = re.findall(r".{4}", fingerprint2)

    combined = []

    for index, value in enumerate(fingerprint_1_parts):
        
        # Parses hex strings to values
        f1 = int(value, 16)
        f2 = int(fingerprint_2_parts[index], 16)

        c = f1 ^ f2

        c_hex = hex(c)[2:].zfill(4)

        combined.append(c_hex)

    return "".join(combined)

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

def create_random_fingerprint(number_of_words):
    return os.urandom(8).hex()

def create_actual_fingerprint_and_key(number_of_words, uncontrolledFingerprint):
    
    biggest_perm_size = 0
    biggest_key = None

    DEBUG_FINGERPRINT = None

    # TODO: Determine number of keys to test
    total_keys = 100

    loop = 0
    for x in range(total_keys):
    
        input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, passphrase="1234")
        key = gpg.gen_key(input_data)
        fp = key.fingerprint

        number_finger_chars = int(number_of_words * 4)
        reduced_fingerprint = fp[-number_finger_chars:]

        combined_fingerprint = XOR_fingerprints(reduced_fingerprint, uncontrolledFingerprint)
        trustWords = fingerprint_to_words(combined_fingerprint, PRINT=False)

        combinations = similar_combinations(trustWords, similar_word_mapping, word_to_hex_mapping)
        perm_size = get_perm_size(combinations)

        if perm_size > biggest_perm_size:
            biggest_key = key
            biggest_perm_size = perm_size
            DEBUG_FINGERPRINT = fp

        loop += 1

        print(f"{loop}/{total_keys} Keys complete", end="\r")

    print()
    print(biggest_perm_size)
    print(gpg.export_keys(biggest_key))
    print(DEBUG_FINGERPRINT)

    # TODO: Fix private key export
    print(gpg.export_keys(biggest_key, secret=True))
    
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

def determine_average_perms(number_of_words, all_perms=True):

    max_perm = 0
    min_perm = None
    loops = 1000000

    total_all = 0
    total_one_static = 0
    total_two_static = 0

    for _ in range(loops):
        fingerprint = create_random_fingerprint(number_of_words)

        trustwords = fingerprint_to_words(fingerprint, PRINT=False)

        if all_perms:
            combinations = similar_combinations(trustwords, similar_word_mapping, word_to_hex_mapping)

            one_static_combinatsions = similar_combinations(trustwords, \
                similar_word_mapping, \
                word_to_hex_mapping, staticPos=[0])

            two_static_combinatsions = similar_combinations(trustwords, \
                similar_word_mapping, \
                word_to_hex_mapping, staticPos=[0, 3])

            perm_len = get_perm_size(combinations)

            # # UNCOMMENT TO Print values out to file
            # print(str(perm_len) + ",")

            one_perm_len = get_perm_size(one_static_combinatsions)
            two_perm_len = get_perm_size(two_static_combinatsions)
        else:
            combinations = multimap_combinations(trustwords, word_to_hex_mapping)
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
    
def PGP_key_hash(key_data):
    # Skips headers and formatting lines
    key_base64 = ""
    for l in key_data[1:-2]:
        key_base64 += l.strip()

    # All the bytes from the key
    key_bytes = base64.b64decode(key_base64)

    # Takes the PGP packey length from the header
    key_length = int.from_bytes(key_bytes[1:3], byteorder="big")

    # Takes the header and length
    key_formatted_bytes = key_bytes[:key_length + 3]

    sha1 = SHA1.new()
    sha1.update(key_formatted_bytes)

    # Takes the left 64-bit
    return sha1.hexdigest()[:16].upper()

def generate_words_for_PGP_keys(key_path_1, key_path_2):
    
    key_data_1 = []
    with open(key_path_1) as key1:
        key_data_1 = key1.readlines()
    
    key_data_2 = []
    with open(key_path_2) as key2:
        key_data_2 = key2.readlines()

    # Takes the left 64-bit
    key_finger_print_1 = PGP_key_hash(key_data_1)
    key_finger_print_2 = PGP_key_hash(key_data_2)

    combined_key = XOR_fingerprints(key_finger_print_1, key_finger_print_2)
    fingerprint_to_words(combined_key)

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
        determine_average_perms(number_of_words)
        exit()

    # Finds number of average multi mapping perms
    if arg.average_multi:
        determine_average_perms(number_of_words, all_perms=False)
        exit()

    # Outputs the trust words for two actual keys
    if arg.trustwords:
        generate_words_for_PGP_keys(arg.trustwords[0], arg.trustwords[1])
        exit()

    if arg.find_keys:
        create_actual_fingerprint_and_key(number_of_words, UNCONTROLLED_FINGERPRINT)
        exit()

    if arg.perms:
        input_string = arg.perms[0]
        input_string = input_string.replace("[", "")
        input_string = input_string.replace("]", "")
        input_string = input_string.replace("\'", "")

        similar_words = []

        words = input_string.split(",")
        words = list(map(str.strip, words))

        for w in words:
            m = similar_word_mapping[w] + [w]
            similar_words.append(m)

        print(similar_words)

        y = get_perms(similar_words)
        print("[!] Permutations: ", len(y))
        exit()

    combined_fingerprint = XOR_fingerprints(CONTROLLABLE_FINGERPRINT, UNCONTROLLED_FINGERPRINT)
    trustwords = fingerprint_to_words(combined_fingerprint)

    # Creates list of multiple mapping
    # i.e. the word "Tree" maps to 0xff43 and 0xf3ee
    if arg.multi:
        perms = multimap_perms(trustwords, word_to_hex_mapping) 
        key_possibilities = find_possible_keys(perms, UNCONTROLLED_FINGERPRINT)
        save_permutations(key_possibilities, outFileName)

    # Default mode of finding all mappings
    else:
        perms = similar_perms(trustwords, similar_word_mapping, word_to_hex_mapping)
        key_possibilities = find_possible_keys(perms, UNCONTROLLED_FINGERPRINT)
        save_permutations(key_possibilities, outFileName)

if __name__ == "__main__":
    args()