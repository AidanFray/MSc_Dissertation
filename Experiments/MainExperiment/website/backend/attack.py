import os
import random
import itertools
import CONFIG

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

def decision():
    
    # If not an attack
    if not random.SystemRandom().random() < CONFIG.ATTACK_CHANCE: 
        return None

    attack_metric_choice = random.SystemRandom().randint(0, 2)
    attack_metric_string = CONFIG.ATTACK_METRICS[attack_metric_choice]

    attack_type_choice = random.SystemRandom().randint(0, 2)

    originalWords = _sample_from_vuln_keys(attack_metric_string, str(attack_type_choice))

    similar_words = load_similar_words(attack_metric_string)

    words = ATTACK_TYPES[attack_type_choice](originalWords, similar_words)

    print("[D] Attack: ", attack_metric_string, attack_type_choice)

    return [attack_metric_string, attack_type_choice, words, originalWords]

def load_similar_words(attackMetricChoice):
    path = f"{CONFIG.BASE_FILE_LOCATION}data/similar/{attackMetricChoice.lower()}.csv"
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

    # TODO: Refactor me 
    MAX_LIST_SIZE = 5000000

    perms = list(itertools.product(
            combinations[0][:MAX_LIST_SIZE], 
            combinations[1][:MAX_LIST_SIZE], 
            combinations[2][:MAX_LIST_SIZE], 
            combinations[3][:MAX_LIST_SIZE])
        )
    print("[D] Perm size: ", len(perms))
    random_match = list(perms[random.randint(0, len(perms) - 1)])
    
    return random_match

def _sample_from_vuln_keys(attackMetric, attackType):

    file_path = f"./data/vuln_keys/{attackMetric.lower()}/{attackMetric.lower()}-static-{attackType}.txt"

    data = None
    with open(file_path, "r") as file:
        data = file.readlines()

    words = random.choice(data).strip().split(" ")

    return words

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
