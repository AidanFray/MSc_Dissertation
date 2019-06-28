import random
import itertools
from CONFIG import BASE_FILE_LOCATION

"""
Each sub attack here will generate a random match from 
the list of combinations:

    `generate_zero_static_word_match`
        - Will generate all permutations of matches while keeping no
          words the same

    `generate_one_static_word_match`
        - Will generate all permutations with the first word kept 
          static

    `generate_two_static_word_match`
        - Will generate all permutations with the first and last
          word kept static

The probability of encountering each of these sub-attacks
is all equal and therefore equally distributed
"""

# To make sure permutations size don't get too big    
MAX_SIMILAR_PERM_SIZE = 100

# 70 / 30 split
ATTACK_CHANCE = 1.0

## NOTE:
#   Naming convension for files is:
#
#       ./data/similar/<lower_case_name>.csv
#
ATTACK_METRICS = ['SOUNDEX', "METAPHONE", "NYSIIS"]

def decision(newWords):
    
    # If not an attack
    if not random.random() < ATTACK_CHANCE: 
        return None

    attack_metric_choice = random.randint(0, 2)
    attack_metric_string = ATTACK_METRICS[attack_metric_choice]

    similar_words = load_similar_words(attack_metric_string)

    attack_type_choice = random.randint(0, 2)
    words = ATTACK_TYPES[attack_type_choice](newWords, similar_words)

    return [attack_metric_string, attack_type_choice, words]

def load_similar_words(attackMetricChoice):
    path = f"{BASE_FILE_LOCATION}data/similar/{attackMetricChoice.lower()}.csv"
    similar_words = {}

    with open(path, "r") as file:

        for line in file:
            line = line.strip()
            line_parts = line.split(",")

            similar_words[line_parts[0]] = line_parts[1:-1]

    return similar_words 

def _get_random_match(words, similarWordsDict, staticPositions):
    combinations = []

    for i, w in enumerate(words):

        possibilities = []

        possibilities.append(w)
        if not i in staticPositions:

            similar_word = [similarWordsDict[w]]

            # This is the make sure the cap isn't bias
            if len(similar_word) > MAX_SIMILAR_PERM_SIZE:
                random.shuffle(similar_word)

            for similarWords in similar_word[:MAX_SIMILAR_PERM_SIZE]:
                for s in similarWords:
                    possibilities.append(s)

        combinations.append(possibilities)

    # print(combinations)
    perms = list(itertools.product(combinations[0], combinations[1], combinations[2], combinations[3]))
    random_match = list(perms[random.randint(0, len(perms))])
    
    return random_match

def generate_zero_static_word_match(words, similarWordsDict):
    return _get_random_match(words, similarWordsDict, staticPositions=[])

def generate_one_static_word_match(words, similarWordsDict):
    return _get_random_match(words, similarWordsDict, staticPositions=[0])

def generate_two_static_word_match(words, similarWordsDict):
    return _get_random_match(words, similarWordsDict, staticPositions=[0, 3])

ATTACK_TYPES = \
    [
        generate_zero_static_word_match, 
        generate_one_static_word_match, 
        generate_two_static_word_match
    ]
