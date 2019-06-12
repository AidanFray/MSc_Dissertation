from scipy.spatial import distance
import pickle
import numpy as np
import time
import sys
import dbm

# DEBUG
WORDVECTOR = "/home/main_user/GitHub/Cyber-Security-Individual-Project/Code/WordVectors/word_vectors.dat"

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
    print(f"[!] Usage: python {__file__} <WORDLIST> <PRE-COMPUTED-DICT> [Optional]")
    exit()

if __name__ == "__main__":
    
    vec_database = {}

    # Checks for minimum number of args
    if len(sys.argv) < 2:
        usage()
     
    word_list = load_wordlist(sys.argv[1])

    # Checks for option args
    if len(sys.argv) < 3:
        print("[*] No dictionary provided, computing a new one")
        
        vec_database = dbm.open(f"database_{int(time.time())}.dbm", "c")
        compute_distances(vec_database, word_list)
    else:
        print("[*] Dictionary provided. Loading data...")
        vec_database = dbm.open(sys.argv[2], 'r')


    #TODO: Search through the dictionary to find the best pair
    for w in vec_database.keys():
        print(w)
        exit()

    # Obtains the best word list
    new_word_list = []

    best_start_vals = sorted_vec_dist[0].split("-")
    new_word_list += best_start_vals

    while len(new_word_list) < NEW_WORDLIST_SIZE:

        best_word = None
        best_avg_distance = None
        for word in word_list:
                
            total_distance = 0
            for w in new_word_list:

                if not word in new_word_list:

                    # Creates the ordered pair ID string
                    word_pair = [word, w]
                    word_pair.sort()

                    total_distance += vec_database[f"{word_pair[0]}-{word_pair[1]}"]

            avg_distance = total_distance / len(new_word_list)

            # Checks for the best value
            if best_avg_distance == None or avg_distance > best_avg_distance:
                best_word = word
                best_avg_distance = avg_distance

        print(f"[*] Best word: {best_word}")
        new_word_list.append(best_word)

    # TODO: Create a function
    with open("new_wordlist.txt", "w") as file:
        for n in new_word_list:
            file.write(n + "\n")