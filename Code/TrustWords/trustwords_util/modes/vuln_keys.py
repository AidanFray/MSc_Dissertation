import sys
sys.path.insert(0, "..")

from util.permutations import *
from util.trustwords import *
from mappings import *

NUM_OF_WORDS = 4

def load_keys_and_parse(filePath):

    keys = []
    with open(filePath) as file:

        for line in file:
            keys.append(line[:NUM_OF_WORDS * 4])

    return keys

def find_vuln_keys(vulnKeyFilePath, mapping, targetNumberOfPerms):
    
    keys = load_keys_and_parse(vulnKeyFilePath)

    trustwords = []
    for k in keys:
        trustwords.append(fingerprint_to_words(k, mapping, PRINT=False))

    # Finds the keys that have the permuataions over our targets
    for t in trustwords:
        num_of_perms = len(similar_perms(t, mapping, PRINT=False))

        if num_of_perms >= targetNumberOfPerms:
            print(t)

    