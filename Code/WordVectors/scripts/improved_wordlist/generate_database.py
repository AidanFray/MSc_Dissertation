from scipy.spatial import distance
import numpy as np
import pickle
import psutil
import time
import sys
import dbm

"""
Script to generate a database of the distances between all the combinations
of words in a dictionary. 
Due to the distance being symmetrical only one value is recorded for a pair.

    i.e. DRAGON-BREAKFAST == BREAKFAST-DRAGON

"""

MAX_RAM_USAGE = 0.10
DECIMAL_PRECISION = 100

WORDVECTOR = "../../word_vectors.dat"

def load_wordvectors():
    """
    Loads the word vectors from file
    """

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
    """
    Calculates the distance between two vectors
    """

    return distance.euclidean(a, b)
    # return distance.cosine(a, b)

def memory_full_check(mem):
    """
    Method to check for the proportion of free RAM
    """

    p = mem.available / mem.total

    if p < MAX_RAM_USAGE:
        return True
    
    return False

def database_sync(database, data_dict, memory_cap=True):
    """
    Syncs the data held in memory to the persistent data object    
    """

    if memory_cap: print("[!] Memory cap reached. Syncing local data to database")
    for d in data_dict:
        database[d] = data_dict[d]

def compute_distances(vec_database, wordlist):
    """
    Computes all the permutations of distances for each combination of words

    The formula for the number of loops is:

         (N^2 / 2)
    """

    print("[*] Loading data....", end="", flush=True)
    word_vec = load_wordvectors()
    print("[OK]")
    print(f"[*] Words loaded: {len(word_list)}")
    
    # This database will hold values localally before being written to the dbm database
    temp_database = {}
    TEMP_SIZE = 10000

    for index1, word1 in enumerate(word_list):

        # index + 1 to avoid itself
        for index2, word2 in enumerate(word_list[index1 + 1:]):

            # Grabs vectors for words
            if word1 in word_vec: word_vec1 = word_vec[word1]
            else: continue

            if word2 in word_vec: word_vec2 = word_vec[word2]
            else: continue

            dist = calc_distance(word_vec1, word_vec2)

            # Adds combination to the dictionary for alphabetic sorting
            dictionary_index = [word1, word2]
            dictionary_index.sort()

            # Values are saved as their index in the wordlist
            # the second words index is worked out from the 
            # offset of itself from the index1

            word1index = index1
            word2index = index1 + index2 + 1

            if dictionary_index[0] == word1:
                dictionary_index_str = f"{word1index}-{word2index}"
            else:
                dictionary_index_str = f"{word2index}-{word1index}"

            # No checks are made for pre-existing values
            # this is because the loop is designed to never overlap
            temp_database[dictionary_index_str] = str(round(dist, DECIMAL_PRECISION))

        mem = psutil.virtual_memory()
        sys.stderr.write(f"[*] {index1}/{len(word_list)} - Memory Available: {round(mem.available / mem.total, 2)}\r")
        sys.stderr.flush()

        if memory_full_check(mem):
            database_sync(vec_database, temp_database)
            temp_database.clear()

    # One final sync
    database_sync(vec_database, temp_database, memory_cap=False)
    temp_database.clear()

def usage():
    print(f"[!] Usage: python {__file__} <WORDLIST>")
    exit()

if __name__ == "__main__":
    
    # Checks for minimum number of args
    if len(sys.argv) != 2:
        usage()

    start_time = time.time()
     
    word_list = load_wordlist(sys.argv[1])

    fileName = f"database_{int(time.time())}.dbm"

    vec_database = dbm.open(fileName, "c")

    compute_distances(vec_database, word_list)
    vec_database.close()

    print(f"\n[!] Execution time: {time.time() - start_time}")

    
