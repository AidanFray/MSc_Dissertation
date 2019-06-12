from scipy.spatial import distance
import pickle
import numpy as np
import time
import sys
import dbm

# DEBUG
WORDVECTOR = "../../word_vectors.dat"

NEW_WORDLIST_SIZE = 256

def load_wordvectors():
    words = {}

    for line in open(WORDVECTOR, encoding="latin-1"):

        line = line.strip()
        word, vector_raw = line.split("  ")

        vector = vector_raw.split(" ")

        # Converts all values from strings to floats
        vector = list(map(float, vector))

        words[word] = np.array([vector])

    return words

def load_wordlist(fileName):
    """
    Loads a wordlist to file
    """

    data = []
    with open(fileName) as file:
        
        for line in file:

            # Formats the line
            line = line.strip()
            line = line.upper()

            data.append(line)

    return data

def calc_distance(a, b):
    return distance.euclidean(a, b)
    # return distance.cosine(a, b)

def compute_distances(vec_database, wordlist):
    print("[*] Loading data....", end="", flush=True)
    word_vec = load_wordvectors()
    print("[OK]")
    print(f"[*] Words loaded: {len(word_list)}")
    
    for index, word1 in enumerate(word_list):

        # index + 1 to avoid itself
        for word2 in word_list[index + 1:]:

            # Grabs vectors for words
            if word1 in word_vec:
                word_vec1 = word_vec[word1]
            else:
                continue

            if word2 in word_vec:
                word_vec2 = word_vec[word2]
            else:
                continue

            dist = calc_distance(word_vec1, word_vec2)

            # Adds combination to the dictionary
            dictionary_index = [word1, word2]
            dictionary_index.sort()

            dictionary_index_str = f"{dictionary_index[0]}-{dictionary_index[1]}"

            if not dictionary_index_str in vec_database:
                vec_database[dictionary_index_str] = str(dist)
            else:
                # Check for accuracy
                pre_existing_distance = vec_database[dictionary_index_str]

                if pre_existing_distance != distance:
                    print(f"[!] Error in distance calculation with words: {word1} and {word2}")

        print(f"[*] {index}/{len(word_list)}", end="\r", flush=True)

def usage():
    print(f"[!] Usage: python {__file__} <WORDLIST>")
    exit()

if __name__ == "__main__":
    
    # Checks for minimum number of args
    if len(sys.argv) != 2:
        usage()
     
    word_list = load_wordlist(sys.argv[1])

    vec_database = dbm.open(f"database_{int(time.time())}.dbm", "c")
    compute_distances(vec_database, word_list)


    
