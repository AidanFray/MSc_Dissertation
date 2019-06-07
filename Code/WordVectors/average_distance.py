from scipy.spatial import distance
import numpy as np
import time
import sys
import os

PRINT_MISSING_WORDS = True
DECIMAL_PRECISION = 3

# How many data points to compute before data is saved
SAVE_PERIOD = 5000000

def load_words():
    words = {}

    for line in open("word_vectors.dat", encoding="latin-1"):

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
        
        # Converts array to string and removes "[" and "]"
        save_string = str(values)[1:-1]

        # Removes spaces to save storage space
        save_string = save_string.replace(" ", "")
        
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

    data_points = []

    total = 0
    loops = 0

    # Creates a directory for periodical saving
    dir_str = init_save()

    num_of_words = len(wordlist)
    for index, word1 in enumerate(wordlist):

        start_time = time.time()

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
            data_points.append(round(distance, DECIMAL_PRECISION))

            loops += 1

            # Saves the data points.
            # This is to prevent large files from filling up all the RAM
            if loops % SAVE_PERIOD == 0:
                save_values(dir_str, data_points)
                data_points.clear()

        end_time = time.time() - start_time;
        total_time_hours = end_time * num_of_words / 3600

        sys.stderr.write(f"{index}/{num_of_words} -- Execution time: {total_time_hours} hours\r")
        sys.stdout.flush()

    # Final save to clean up any leftover values
    save_values(dir_str, data_points)

    print()
    print("#" * 40)
    print(f"AVERAGE: {total/loops}")
    print("#" * 40)

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