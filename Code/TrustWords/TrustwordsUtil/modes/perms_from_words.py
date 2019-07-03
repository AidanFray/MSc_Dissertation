import sys

sys.path.insert(0, "..")

from mappings import *
from util.permutations import *

def num_of_perms_of_words(trustwords, mapping):
    trustwords = trustwords.replace("[", "")
    trustwords = trustwords.replace("]", "")
    trustwords = trustwords.replace("\'", "")

    similar_words = []

    words = trustwords.split(",")
    words = list(map(str.strip, words))

    for w in words:
        m = mapping.getMapping(MappingModes.SimilarWord, w) + [w]
        similar_words.append(m)

    y = get_perms(similar_words)
    print("[!] Permutations: ", len(y))