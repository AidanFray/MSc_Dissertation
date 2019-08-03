import sys

sys.path.insert(0, "..")

from util.mappings import *
from util.permutations import *

def num_of_perms_of_words(trustwords, mapping, PRINT=True):
    trustwords = trustwords.replace("[", "")
    trustwords = trustwords.replace("]", "")
    trustwords = trustwords.replace("\'", "")
    trustwords = trustwords.replace(",", "")

    similar_words = []

    words = trustwords.split(" ")
    words = list(map(str.strip, words))

    perms = similar_perms_size(words, mapping)

    if PRINT: print("[!] Permutations: ", perms)

    return perms