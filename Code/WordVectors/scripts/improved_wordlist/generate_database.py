from scipy.spatial import distance
import numpy as np
# import pickle
import time
import sys
import dbm

"""
Script to generate a database of the distances between all the combinations
of words in a dictionary. 
Due to the distance being symmetrical only one value is recorded for a pair.

    i.e. DRAGON-BREAKFAST == BREAKFAST-DRAGON

"""

# Precision for the saved float values
DECIMAL_PRECISION = 3
WORDVECTOR_PATH = "../../word_vectors.dat"

def load_wordvectors():
    """
    Loads the word vectors from file
    """

    words = {}

    for line in open(WORDVECTOR_PATH, encoding="latin-1"):

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
        
def compute_distances(database_filepath, wordlist):
    """
    Computes all the permutations of distances for each combination of words

    The formula for the number of loops is:

         (N^2 / 2)
    """

    TIME_CALCULATED = False
    NUM_OF_LOOPS_BEFORE_CHECK = 50000

    loops = 0

    print("[*] Loading data....", end="", flush=True)
    word_vec = load_wordvectors()
    print("[OK]")
    num_of_words = len(wordlist)
    print(f"[*] Words loaded: {num_of_words}")
    
    # This database will hold values localally before being written to the dbm database
    database = dbm.open(database_filepath, "c")

    start_time = time.time()

    for index1, word1 in enumerate(word_list):

        # index + 1 to avoid itself
        for index2, word2 in enumerate(word_list[index1 + 1:]):

            # Grabs vectors for words. The loop is ignored if the
            # word isn't present
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
            database[dictionary_index_str] = str(round(dist, DECIMAL_PRECISION))

            if not TIME_CALCULATED and loops == NUM_OF_LOOPS_BEFORE_CHECK:
                run_time_calc(start_time, num_of_words, loops)
                TIME_CALCULATED = True
            
            loops += 1

        sys.stderr.write(f"[*] {index1}/{len(word_list)}\r")
        sys.stderr.flush()

def run_time_calc(start_time, num_of_words, completed_loops):

    total_loops = (pow(num_of_words, 2) / 2) + (num_of_words / 2)

    end_time = (time.time() - start_time) / completed_loops
    total_time_hours = end_time * total_loops / 3600
    print(f"[!] Estimated execution time: {round(total_time_hours, 2)} hours")

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

    # Creates the database object
    dbm.open(fileName, "c").close()

    compute_distances(fileName, word_list)

    print(f"\n[!] Execution time: {time.time() - start_time}")