words = []

def lev_distance(word1, word2):
    
    diff = 0

    len_diff = abs(len(word1) - len(word2))

    # Deals with different length strings
    if len(word1) > len(word2):
        min_len = len(word2)
        min_word = word1
        max_word = word2
    else:
        min_len = len(word1)
        min_word = word2
        max_word = word1

    for x in range(min_len):

        if min_word[x] != max_word[x]:
            diff += 1
    
    # Adds on the remaining letters
    diff += len_diff
    print(f"[*] Difference between: {min_word} and {max_word} is: {diff}")



with open("./en.csv") as file:
    data = file.readlines()

for line in data:
    parts = line.split(",")
    words.append(parts[2])

# Converts all strings to lower
words = list(map(str.lower, words))

for x in range(len(words) - 1):
    lev_distance(words[x], words[x + 1])


