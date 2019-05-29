import jellyfish
import numpy as np
import timeit

algorithm_and_weights = \
[
    [jellyfish.soundex, 1],
    [jellyfish.match_rating_codex, 1],
    [jellyfish.metaphone, 1],
    [jellyfish.nysiis, 1]
]

similarity_tolerance = 3.0

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def similar(word1, word2):
    total= 0.0
    for aw in algorithm_and_weights:

        al = aw[0]
        w  = aw[1]

        code1 = al(word1)
        code2 = al(word2)
        lev = levenshtein(code1, code2)
        subtotal = lev * w
        total += subtotal

    return total

words = None
with open("../Wordlists/EN/en_unique.csv") as file:
    words = file.readlines()

# Cleans the words of their newline characters
words = list(map(str.strip, words))

# Vars
number_of_words = len(words)
words_complete = 0

for word1 in words:

    start = timeit.default_timer()
    for word2 in words:

        if word1 != word2:
            s = similar(word1, word2)

            if s <= similarity_tolerance:
                print(word1, word2, s)
            
    stop = timeit.default_timer()
    # print("[!] Time to complete: ", (stop-start)*number_of_words / 3600)

    words_complete += 1