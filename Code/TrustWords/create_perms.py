import re
import itertools

##################################################
#                   TODO                         #
##################################################
# - Work out average number of combinations of
#   keys. This can be used to give a rough idea
#   of feasibility
#
# - Add dynamic code to allow easy swapping 
#   between Full, Long or Short mapping
#
# - Re-factor and comment code
###################################################

file_path = "/home/user/Github/Cyber-Security-Individual-Project/Code/TrustWords" # DEBUG
# file_path = ".."

TARGET_FINGERPRINT = "FD08D9E0AF3386B658981EFCC0FFEEC0FFEE2D4F"       # 2433024
# TARGET_FINGERPRINT = "107C21DDB023B2959A5B21F4C0FFEE63D83FBEEF"       # 41472
# TARGET_FINGERPRINT = "2F88CE861A1B19D35F804A15197BF4412139696F"       # 718848
# TARGET_FINGERPRINT = "843938DF228D22F7B3742BC0D94AA3F0EFE21092"       # 86016
# TARGET_FINGERPRINT = "C5986B4F1257FFA86632CBA746181433FBB75451"       # 129472


mappings_hex_to_word = {}
mappings_word_to_hex = {}

def load_mappings():

    with open(f"{file_path}/en.csv") as file:

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

def load_similar_mappings():

    mappings_similar_words = {}

    with open(f"{file_path}/similar.csv") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        line_parts = line.split(",")

        base_word = line_parts[0]
        similar_words = line_parts[1:-1]

        mappings_similar_words.update({base_word : similar_words})

    return mappings_similar_words

def finger_print_to_words(fingerprint):

    trustwords = []

    chunks = re.findall(".{4}", fingerprint)

    print("#" * 100)

    for chunk in chunks:
        word = mappings_hex_to_word[chunk.lower()]
        trustwords.append(word)
        print(word, end=" ")
    
    print()
    print("#" * 100)

    return trustwords

def gen_overlapping_trustwords(trustwords):
    print()

    fingerprint_chunks = []
    for words in trustwords:

        perms = []
        for w in words:
            chunk = mappings_word_to_hex[w]
            perms += chunk

        fingerprint_chunks.append(perms)

    x = create_all_permutations(fingerprint_chunks)

    return x

def gen_similar_trust_words(trustwords):
    
    similar_words = []
    mappings_similar_words = load_similar_mappings()

    for word in trustwords:

        try:
            similar_words.append(mappings_similar_words[word])
        
        # No similar words
        except KeyError:
            similar_words.append([])

    for index, _ in enumerate(similar_words):
        similar_words[index].append(trustwords[index])            

    y = gen_overlapping_trustwords(similar_words)

    print(f"[*] Mapping allows {len(y)} different combinations!")

def create_all_permutations(lists):
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

if __name__ == "__main__":
    load_mappings()
    trustwords = finger_print_to_words(TARGET_FINGERPRINT)
    gen_similar_trust_words(trustwords)
