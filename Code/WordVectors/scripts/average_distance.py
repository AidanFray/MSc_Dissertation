from scipy.spatial import distance
import numpy as np
import time
import sys
import os

PRINT_MISSING_WORDS = False
DECIMAL_PRECISION = 3

# How many data points to compute before data is saved
SAVE_PERIOD = 5000000

def load_words():
    words = {}

    for line in open("../word_vectors.dat", encoding="latin-1"):

        line = line.strip()
        word, vector_raw = line.split("  ")

        vector = vector_raw.split(" ")

        # Converts all values from strings to floats
        vector = list(map(float, vector))

        words[word] = np.array([vector])

    return words

def load_wordlist(wordlistPath):
    wordlist = []
    with open(f"{wordlistPath}") as file:
        wordlist = file.readlines()
    
    wordlist = list(map(str.upper, wordlist))
    wordlist = list(map(str.strip, wordlist))

    return wordlist

def init_save():
    # Saves data to file name
    dir_str = int(time.time())

    os.system(f"mkdir {dir_str}")

    return dir_str

def save_values(dir_str, values):
    with open(f"{dir_str}/values.dat", "a") as file:
        
        for v in values:
            save_string = f"{v}: {values[v]}\n"
            file.write(save_string)

def calc_distance(a, b):
    return distance.euclidean(a, b)

def calc_missing_words(wordlist, word_vec):

    missing_words = []

    for w in wordlist:
        if not w in word_vec:
            missing_words.append(w)

    return missing_words

def calculate_average(wordlist, word_vec):

    # Holds a tally of the number of values
    data_points_count = {}

    num_of_words = len(wordlist)

    TIME_CALCULATED = False

    # Takes an average of the loops to get a better time calc
    NUM_OF_LOOPS_BEFORE_CHECK = int(num_of_words * 0.1)

    total = 0
    loops = 0

    # Creates a directory for periodical saving
    dir_str = init_save()

    if not TIME_CALCULATED: start_time = time.time()

    for index, word1 in enumerate(wordlist):

        # index + 1 to avoid itself
        for word2 in wordlist[index + 1:]:

            if word1 in word_vec:
                word_vec1 = word_vec[word1]
            else:
                continue

            if word2 in word_vec:
                word_vec2 = word_vec[word2]
            else:
                continue

            distance = calc_distance(word_vec1, word_vec2)
            total += distance

            # Adds values to the dictionary
            distance = round(distance, DECIMAL_PRECISION)
            if not distance in data_points_count:
                data_points_count[distance] = 1
            else:
                data_points_count[distance] += 1


            if not TIME_CALCULATED and loops == NUM_OF_LOOPS_BEFORE_CHECK:
                total_loops = (pow(num_of_words, 2) / 2) + (num_of_words / 2)

                end_time = (time.time() - start_time) / NUM_OF_LOOPS_BEFORE_CHECK
                total_time_hours = end_time * total_loops / 3600
                print(f"[!] Estimated execution time: {round(total_time_hours, 2)} hours")
                TIME_CALCULATED = True

            loops += 1

        sys.stderr.write(f"[*] {index}/{num_of_words}\r")
        sys.stdout.flush()

    save_values(dir_str, data_points_count)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: ./average_distance <WORD_LIST>")
        exit()

    wordlistPath = sys.argv[1]

    print("[!] Loading data.....", end="")
    sys.stdout.flush()
    word_vec = load_words()
    wordlist = load_wordlist(wordlistPath)
    print("[OK]")


    # # Prints out non-represented words
    missing_words = calc_missing_words(wordlist, word_vec)
    if PRINT_MISSING_WORDS:
        if len(missing_words) != 0:
            print(f"[!] We have {len(missing_words)} non represented words!")
            for w in missing_words: print(w)
            exit(0)

    calculate_average(wordlist, word_vec)