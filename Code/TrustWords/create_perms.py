import re
import itertools
import argparse
from Crypto.Hash import SHA1
import os

##################################################
# TODO - Functionality to change fingerprints via
#        the command line
##################################################

# DEBUG - For VSCode
# file_path = "/home/main_user/GitHub/Cyber-Security-Individual-Project/Code/TrustWords" 
file_path = "."

# The fingerprint of the target
UNCONTROLLED_FINGERPRINT    = "7E6C 4BF0 5CE3 F379"

# The fingerprint we can change via MITM
CONTROLLABLE_FINGERPRINT    = "2F88 CE86 1A1B 19D4"

# Stops the program from generating permutations that fill the RAM
MAX_PEM_SIZE = 2000000000

mappings_hex_to_word = {}
mappings_word_to_hex = {}
mappings_similar_words = {} 

def load_mappings(fileName):
    """
    Loads the hex -> word mapping into a local dictionary
    """

    with open(f"{file_path}/{fileName}") as file:

        line = None
        while True:
            line = file.readline()
            if line == '': break
            
            line_parts = line.split(",")

            # Maps string to 
            word                =  line_parts[2]
            word_hex    =  hex(int(line_parts[1]))[2:].zfill(4)

            # Hex --> Word
            mappings_hex_to_word.update({word_hex : word})

            # Word --> Hex
            if word in mappings_word_to_hex:
                mappings_word_to_hex[word].append(word_hex)
            else:
                mappings_word_to_hex.update({word : [word_hex]})
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

        mappings_similar_words.update({base_word : similar_words})

def save_permutations(perms):
    """
    Saves the potential key permutations to file
    """

    with open("./target_keys.txt", "w") as file:
        for p in perms:
            file.write(p.lower())
            file.write("\n")

def finger_print_to_words(fingerprint, PRINT=True):
    """
    Maps the hex value of the key to a word defined in
    the dictionary loaded
    """

    fingerprint = fingerprint.replace(" ", "")

    trustwords = []

    chunks = re.findall(".{4}", fingerprint)

    for chunk in chunks:
        word = mappings_hex_to_word[chunk.lower()]
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

def find_possible_keys(perms):
    """
    This method is used to produce a list of key fingerprints that would be near
    matches to the valid fingerprints
    """

    key_possibilities = []
    for p in perms:

        possible_fingerprint = "".join(p)

        f = XOR_fingerprints(possible_fingerprint, UNCONTROLLED_FINGERPRINT)

        key_possibilities.append(f)

    return key_possibilities

def gen_all_same_perms(wordlist, PRINT=True):
    mappings = gen_all_same_combinations(wordlist)

    if check_perm_size(mappings):
        perms = gen_permutations(mappings)
        if PRINT: print(f"[*] Mapping allows {len(perms)} same combinations!")

    return perms
def gen_all_same_combinations(wordlist):
    mappings = []

    for word in wordlist:
        mappings.append(mappings_word_to_hex[word])

    return mappings

def gen_all_similar_perms(trustwords, PRINT=True):
    """
    This method takes multi-mappings (Same word multiple value) and
    similar words and creates all the permutations of fingerprints
    that allow these near matches
    """

    fingerprint_chunks = gen_all_similar_combinations(trustwords)
    
    output_perms = []
    if check_perm_size(fingerprint_chunks):
        output_perms = gen_permutations(fingerprint_chunks)
        if PRINT: print(f"[*] Mapping allows {len(output_perms)} similar combinations!")

    return output_perms
def gen_all_similar_combinations(trustwords):
    similar_words = []

    # Finds all similar words from the current fingerprint
    for word in trustwords:

        try:
            similar_words.append(mappings_similar_words[word])
        
        # No similar words
        except KeyError:
            similar_words.append([])

    for index, _ in enumerate(similar_words):
        # Adds the original words to the lists
        similar_words[index].append(trustwords[index])

    # Then finds all multi-mapped words and calculates the full number of perms
    fingerprint_chunks = []
    for words in similar_words:

        perms = []
        for w in words:
            chunk = mappings_word_to_hex[w]
            perms += chunk

        fingerprint_chunks.append(perms)

    return fingerprint_chunks

def gen_permutations(lists):
    """
    This method uses ittertools to create all the
    permutations of fingerprints
    """

    perm_size = 1
    for l in lists:
        perm_size *= len(l) 

    size = len(lists)

    # Full mapping
    if size == 10:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                    lists[4],
                    lists[5],
                    lists[6],
                    lists[7],
                    lists[8],
                    lists[9]
                ))

    # Long mapping
    if size == 9:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                    lists[4],
                    lists[5],
                    lists[6],
                    lists[7],
                    lists[8],
                ))

    # Short mapping
    elif size == 5:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                    lists[4],
                ))

    # Minimum size
    elif size == 4:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                ))
    else:
        raise Exception("Invalid permutation size!")
def check_perm_size(lists):
    perm_size = get_perm_size(lists)

    if perm_size > MAX_PEM_SIZE:
        print(f"[!] Permutation too big at: {perm_size}. Ignoring due to RAM constraints")
        return False
    else:
        return True
def get_perm_size(lists):
    perm_size = 1
    for l in lists:
        perm_size *= len(l) 

    return perm_size

def create_random_fingerprint(number_of_words):
    sha = SHA1.new()
    sha.update(os.urandom(10))
    digest = sha.hexdigest()

    return digest[:number_of_words *  4]
def determine_average_perms(number_of_words, all_perms=True):

    max_perm = 0
    min_perm = None
    loops = 100000
    total = 0

    for x in range(loops):
        fingerprint = create_random_fingerprint(number_of_words)
        trustwords = finger_print_to_words(fingerprint, PRINT=False)

        if all_perms:
            combinations = gen_all_similar_combinations(trustwords)
            perm_len = get_perm_size(combinations)
        else:
            combinations = gen_all_same_combinations(trustwords)
            perm_len = get_perm_size(combinations)
        
        # MAX
        if perm_len > max_perm:
            max_perm = perm_len

        # MIN
        if min_perm == None or perm_len < min_perm:
            min_perm = perm_len

        total += perm_len

    print(f"[!] Average permutations is: {total / loops}")
    print(f"[!] Max: {max_perm}")
    print(f"[!] Min: {min_perm}")

def args():
    parser = argparse.ArgumentParser(description='Compute similar TrustWord keys')

    parser.add_argument("--multi", dest="multi", action="store_true")
    parser.add_argument("--average-multi", dest="average_multi", action="store_true")
    parser.add_argument("--average", dest="average", action="store_true")
    parser.add_argument("-l", dest="language", nargs=1, action="store")
    parser.add_argument("-sm", dest="similar", nargs=1, action="store")
    parser.add_argument("-n", dest="num_words", nargs=1, type=int, action="store")

    args = parser.parse_args()

    language = "en"
    if args.language:
        language = args.language[0]

    number_of_words = 4
    if args.num_words:
        number_of_words = args.num_words[0]

    # Loads the file paths
    if args.similar:
        similar_mappings_file_name = args.similar[0]
    else:
        similar_mappings_file_name = f"Wordlists/{language.upper()}/{language.lower()}_similar.csv"

    dictionary_file_name = f"Wordlists/{language.upper()}/{language.lower()}.csv"

    load_mappings(dictionary_file_name)
    load_similar_mappings(similar_mappings_file_name)

    # Finds number of average multi mapping perms
    if args.average_multi:
        determine_average_perms(number_of_words, all_perms=False)

    # Average number of potential keys
    elif args.average:
        determine_average_perms(number_of_words)

    # Default is a calculation of all combinations
    else:
        combined_fingerprint = XOR_fingerprints(CONTROLLABLE_FINGERPRINT, UNCONTROLLED_FINGERPRINT)
        trustwords = finger_print_to_words(combined_fingerprint)

        if args.multi:
            perms = gen_all_same_perms(trustwords) 
            key_possibilities = find_possible_keys(perms)
            save_permutations(key_possibilities)
        else:
            perms = gen_all_similar_perms(trustwords)
            key_possibilities = find_possible_keys(perms)
            save_permutations(key_possibilities)

if __name__ == "__main__":
    args()