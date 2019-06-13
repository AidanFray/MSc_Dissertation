from scipy.spatial import distance
from multiprocessing import Process, Lock
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

PROCCESSES = []

RUNNING_DATABASE_THREAD = None

MAX_RAM_USAGE = 0.60
DECIMAL_PRECISION = 3

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

def spawn_database_sync_thread(database_filepath, data_dict):
    
    p = Process(target=database_sync, args=(database_filepath, data_dict,))
    p.start()
    PROCCESSES.append(p)
    
def database_sync(database_filepath, data_dict):
    """
    Syncs the data held in memory to the persistent data object    
    """

    database = dbm.open(database_filepath, "c")

    print(f"\n[D] Saving {len(data_dict)} datapoints")
    for d in data_dict:
        database[d] = data_dict[d]

    database.close()

def wait_for_processes_to_finish():
    for proc in PROCCESSES:
        proc.join()

def count_active_procs():

    for index, p in enumerate(PROCCESSES):

        if not p.is_alive():
            del PROCCESSES[index]

    return len(PROCCESSES)

def compute_distances(database_filename, wordlist):
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

        number_of_processes = count_active_procs()

        mem = psutil.virtual_memory()
        sys.stderr.write(f"[*] {index1}/{len(word_list)} - Memory Available: {round(mem.available / mem.total, 2)} -- Active Procs: {number_of_processes}\r")
        sys.stderr.flush()

        if number_of_processes == 0:
            if memory_full_check(mem):
                spawn_database_sync_thread(database_filename, temp_database)
                temp_database.clear()

    # One final sync
    print("[*] Syncing finial values...", end="", flush=True)
    spawn_database_sync_thread(database_filename, temp_database)
    temp_database.clear()
    print("[OK]")

    wait_for_processes_to_finish()

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