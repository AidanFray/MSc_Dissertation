import sys
sys.path.append("..")
sys.path.append("./trustword_util/util")

from util.permutations import *
from util.trustwords import *
from util.mappings import *
from util.load import *

NUM_OF_WORDS = 4

def load_keys_and_parse(filePath):

    keys = []
    with open(filePath) as file:

        for line in file:
            keys.append(line[:NUM_OF_WORDS * 4])

    return keys

def find_vuln_keys(vulnKeyFilePath, targetNumberOfPerms, staticWordsVal, mapping):
    
    keys = load_keys_and_parse(vulnKeyFilePath)

    static_pos = []
    if staticWordsVal == 2:
        static_pos = [0, 3]
    elif staticWordsVal == 1:
        static_pos = [0]

    total_loops = len(keys)

    for i, k in enumerate(keys):
        trustwords = fingerprint_to_words(k, mapping, PRINT=False)

        num_of_perms = similar_perms_size(trustwords, mapping, staticPos=static_pos)

        # num_of_perms == 0 is when RAM protection activates
        if num_of_perms >= targetNumberOfPerms or num_of_perms == 0:
            print(" ".join(trustwords))

        sys.stderr.write(f"{i}/{total_loops}\r")