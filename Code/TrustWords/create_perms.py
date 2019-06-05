import re
import itertools
import argparse
from Crypto.Hash import SHA1
import os
import base64
import gnupg

##################################################
# TODO: Fingerprints found via brute force 
#       `--find-key` option don't have the correct
#       number of perms?
##################################################

# DEBUG - For VSCode
# file_path = "/home/main_user/GitHub/Cyber-Security-Individual-Project/Code/TrustWords" 
file_path = "."

# GPG object
gpg = gnupg.GPG(options=["--debug-quick-random"])

# Stops the program from generating permutations that fill the RAM
MAX_PEM_SIZE = 200000000000

# Around a RX480
HASHSPEED = 2000

mappings_hex_to_word = {}
mappings_word_to_hex = {}
mappings_similar_words = {} 

def timing(length_in_chars, permutations):
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

def save_permutations(perms, outFileName):
    """
    Saves the potential key permutations to file
    """

    with open(f"./{outFileName}", "w") as file:
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
    sha.update(os.urandom(15))
    digest = sha.hexdigest()

    return digest[:number_of_words *  4]
def create_actual_fingerprint_and_key(number_of_words):
    
    biggest_perm_size = 0
    biggest_key = None

    # TODO: Determine number of keys to test
    total_keys = 1

    loop = 0
    for x in range(total_keys):
    
        input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, passphrase="1234")
        key = gpg.gen_key(input_data)
        fp = key.fingerprint

        number_finger_chars = int(number_of_words * 4)
        reduced_fingerprint = key.fingerprint[:number_finger_chars]

        words = finger_print_to_words(reduced_fingerprint, PRINT=False)
        combinations = gen_all_similar_combinations(words)
        perm_size = get_perm_size(combinations)

        if perm_size > biggest_perm_size:
            biggest_key = key
            biggest_perm_size = perm_size

        loop += 1

        print(f"{loop}/{total_keys} Keys complete", end="\r")



    print()
    print(biggest_perm_size)
    print(gpg.export_keys(key))

    # TODO: Fix private key export
    # print(gpg.export_keys(key, secret=True))
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

    return " ".join(formatted_fingerprint[:number_of_words])

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

    average_perm = total / loops

    # 4 hex chars per word
    number_of_characters = float(number_of_words * 4)

    min_time = timing(number_of_characters, min_perm)
    max_time = timing(number_of_characters, max_perm)

    average_time = timing(number_of_characters, average_perm) 

    print(f"[!] At a speed of {HASHSPEED}MH/s")
    print(f"[!] Average permutations is: {average_perm}")
    print_timing(average_time)

    print(f"[!] Max: {max_perm}")
    print_timing(max_time)

    print(f"[!] Min: {min_perm}")
    print_timing(min_time)
    
def generate_words_for_PGP_keys(key_path_1, key_path_2):
    
    # TODO: Add ability to pass the first key
    # key_data_1 = []
    # with open(key_path_1) as key1:
    #     key_data_1 = key1.readlines()
    
    # TEMP
    key_finger_print_1 = "7E6C 4BF0 5CE3 F379".replace(" ", "")

    key_data_2 = []
    with open(key_path_2) as key2:
        key_data_2 = key2.readlines()

    key_base64_2 = ""

    # Skips headers and formatting lines
    for l in key_data_2[1:-2]:
        key_base64_2 += l.strip()

    # All the bytes from the key
    bytes_2 = base64.b64decode(key_base64_2)

    # Takes the PGP packey length from the header
    key_length = int.from_bytes(bytes_2[1:3], byteorder="big")

    # Takes the header and length
    key_bytes_2 = bytes_2[:key_length + 3]

    sha1 = SHA1.new()
    sha1.update(key_bytes_2)

    # Takes the left 64-bit
    key_finger_print_2 = sha1.hexdigest()[:16].upper()

    combined_key = XOR_fingerprints(key_finger_print_1, key_finger_print_2)
    finger_print_to_words(combined_key)

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
    parser.add_argument("-t", "--trustwords", dest="keys", nargs=2, action="store")
    parser.add_argument("-f", "--find-keys", dest="find_keys", action="store_true")
    
    # Params
    parser.add_argument("-k", "--key", dest="key", nargs=1, action="store")
    parser.add_argument("-s", "--similar-wordlist", dest="similar", nargs=1, action="store")
    parser.add_argument("-l", "--langauge", dest="lang", nargs=1, action="store")
    parser.add_argument("-n","--num-of-words", dest="num_words", nargs=1, type=int, action="store")
    parser.add_argument("-o", "--output-file-name", dest="output", nargs=1, action="store")
    args = parser.parse_args()


    # Number of words
    number_of_words = args.num_words[0] if args.num_words else 4

    # Output file name
    outFileName = args.output[0] if args.output else "target_keys.txt"

    if args.key:
        CONTROLLABLE_FINGERPRINT = load_key_from_file_and_return_fingerprint(args.key[0], number_of_words)

    # Loads the file paths for similar wordlist
    if args.similar: 
        similar_mappings_file_name = args.similar[0]
        load_similar_mappings(similar_mappings_file_name)
    else:
        # Average multi and multi options do not require a similar wordlist
        if not args.average_multi or args.multi:
            print("[!] Please include similar wordlist!")
            exit()

    # Sets the dictionary mapping file - Default is english
    dictionary_file_name = f"Wordlists/{args.lang[0].upper()}/{args.lang[0].lower()}.csv" \
        if args.lang else f"Wordlists/EN/en.csv"
    load_mappings(dictionary_file_name)

    ### MODES ###
    # Average number of potential keys
    if args.average:
        determine_average_perms(number_of_words)
        exit()

    # Finds number of average multi mapping perms
    if args.average_multi:
        determine_average_perms(number_of_words, all_perms=False)
        exit()

    # Outputs the trust words for two actual keys
    if args.keys:
        generate_words_for_PGP_keys(args.keys[0], args.keys[1])
        exit()

    if args.find_keys:
        create_actual_fingerprint_and_key(number_of_words)
        exit()

    combined_fingerprint = XOR_fingerprints(CONTROLLABLE_FINGERPRINT, UNCONTROLLED_FINGERPRINT)
    trustwords = finger_print_to_words(combined_fingerprint)

    # Creates list of multiple mapping
    # i.e. the word "Tree" maps to 0xff43 and 0xf3ee
    if args.multi:
        perms = gen_all_same_perms(trustwords) 
        key_possibilities = find_possible_keys(perms, UNCONTROLLED_FINGERPRINT)
        save_permutations(key_possibilities, outFileName)

    # Default mode of finding all mappings
    else:
        perms = gen_all_similar_perms(trustwords)
        key_possibilities = find_possible_keys(perms, UNCONTROLLED_FINGERPRINT)
        save_permutations(key_possibilities, outFileName)

if __name__ == "__main__":
    args()