import re
import itertools

TARGET_FINGERPRINT = "107C21DDB023B2959A5B21F4C0FFEE63D83FBEEF"

mappings_hex_to_word = {}
mappings_word_to_hex = {}

def load_mappings():

    mappings_file_path = "/home/user/Github/Cyber-Security-Individual-Project/Code/TrustWords"
    # mappings_file_path = ".."

    with open(f"{mappings_file_path}/en.csv") as file:

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

def gen_similar_trustwords(trustwords):
    print()

    fingerprint_chunks = []
    for word in trustwords:
        chunk = mappings_word_to_hex[word]
        fingerprint_chunks.append(chunk)

    # TODO: More dynamic way to do this
    x = list(itertools.product( \
        fingerprint_chunks[0],
        fingerprint_chunks[1],
        fingerprint_chunks[2],
        fingerprint_chunks[3],
        fingerprint_chunks[4],
        fingerprint_chunks[5],
        fingerprint_chunks[6],
        fingerprint_chunks[7],
        fingerprint_chunks[8],
        fingerprint_chunks[9]
    ))
    print(f"[*] Mapping allows {len(x)} different combinations!")


if __name__ == "__main__":
    load_mappings()
    trustwords = finger_print_to_words(TARGET_FINGERPRINT)
    gen_similar_trustwords(trustwords)