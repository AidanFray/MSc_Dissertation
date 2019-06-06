import numpy as np
from scipy.spatial import distance
import sys

PRINT_MISSING_WORDS = False

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

def calc_distance(a, b):
    return distance.euclidean(a, b)

def calculate_average(wordlistPath):

    non_represented_words = {}

    print("[!] Loading data.....", end="")
    sys.stdout.flush()
    word_vec = load_words()
    wordlist = load_wordlist(wordlistPath)
    print("[OK]")


    total = 0
    loops = 0

    num_of_words = len(wordlist)
    for index, word1 in enumerate(wordlist):

        for word2 in wordlist[index:]:
            
            try:
                word_vec1 = word_vec[word1]
            except KeyError as e:
                word_str = e.args[0]
                if not word_str in non_represented_words:
                    non_represented_words[word_str] = ""

            try:
                word_vec2 = word_vec[word2]
            except KeyError as e:
                word_str = e.args[0]
                if not word_str in non_represented_words:
                    non_represented_words[word_str] = ""

            total += calc_distance(word_vec1, word_vec2)

            loops += 1

        # # Prints out non-represented words
        if PRINT_MISSING_WORDS:
            if len(non_represented_words) != 0:
                print("[!] We have non represented words!")
                for w in non_represented_words:
                    print(w)
                exit(0)

        print(f"{index}/{num_of_words} -- Non represented words {len(non_represented_words)}", end="\r")

    print()
    print("#" * 40)
    print(f"AVERAGE: {total/loops}")
    print("#" * 40)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: ./average_distance <WORD_LIST>")
        exit()

    wordlistPath = sys.argv[1]

    calculate_average(wordlistPath)