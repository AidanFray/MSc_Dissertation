import sys

sys.path.insert(0, "..")

from mappings import *
from util.permutations import *

def num_of_perms_of_words(trustwords, mapping):
    trustwords = trustwords.replace("[", "")
    trustwords = trustwords.replace("]", "")
    trustwords = trustwords.replace("\'", "")
    trustwords = trustwords.replace(",", "")


    similar_words = []

    words = trustwords.split(" ")
    words = list(map(str.strip, words))

    print("[!] Permutations: ", similar_perms_size(words, mapping))