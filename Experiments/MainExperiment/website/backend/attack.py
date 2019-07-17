import os
import random
import itertools
import CONFIG

from trustwords_util.util import load, permutations, trustwords, mappings

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
MAX_SIMILAR_PERM_SIZE = 5000000

def decision():
    
    # If not an attack
    if not random.SystemRandom().random() < CONFIG.ATTACK_CHANCE: 
        return None

    attack_metric_choice = random.SystemRandom().randint(0, 2)
    attack_metric_string = CONFIG.ATTACK_METRICS[attack_metric_choice]

    attack_type_choice = random.SystemRandom().randint(0, 2)

    originalWords = _sample_from_vuln_keys(attack_metric_string, str(attack_type_choice))

    m = mappings.Mappings()

    load.load_mappings("./data/en.csv", m)
    load.load_similar_mappings(f"./data/similar/{attack_metric_string.lower()}.csv", m)

    words = ATTACK_TYPES[attack_type_choice](originalWords, m)

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

def _get_random_match(words, mapping, staticPositions):

    fingerprintChunks = permutations.similar_perms(words, mapping, PRINT=False, staticPos=staticPositions)   

    print("[D] Words:", words)
    print("[D] similar_perms(): ", len(fingerprintChunks))
    print("[D] similar_perms_size(): ", permutations.similar_perms_size(words, mapping, staticPos=staticPositions))

    chunkChoice = random.choice(fingerprintChunks)

    return trustwords.fingerprint_to_words("".join(chunkChoice), mapping, PRINT=False)


def _sample_from_vuln_keys(attackMetric, attackType):

    file_path = f"./data/vuln_keys/{attackMetric.lower()}/{attackMetric.lower()}-static-{attackType}.txt"

    data = None
    with open(file_path, "r") as file:
        data = file.readlines()

    words = random.choice(data).strip().split(" ")

    return words

def generate_zero_static_word_match(words, mapping):
    return _get_random_match(words, mapping, staticPositions=[])

def generate_one_static_word_match(words, mapping):
    return _get_random_match(words, mapping, staticPositions=[0])

def generate_two_static_word_match(words, mapping):
    return _get_random_match(words, mapping, staticPositions=[0, 3])

ATTACK_TYPES = \
    [
        generate_zero_static_word_match, 
        generate_one_static_word_match, 
        generate_two_static_word_match
    ]
