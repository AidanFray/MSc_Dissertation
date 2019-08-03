import sys
import os
import pickle

sys.path.append("/home/main_user/GitHub/Cyber-Security-Individual-Project/Code/TrustwordUtil")
sys.path.append("..")

import experiment
from util.mappings import Mappings
from util.permutations import *
from util.load import *

from modes.perms_from_words import *


"""
    Script that checks that the number of permutations per attack
    are correct
"""

#            Leven       NYSIIS     Metaphone
mapObjects = {"LEVEN": Mappings(), "NYSIIS": Mappings(), "METAPHONE": Mappings()}

attackTypes = {0: 15250, 1: 1525, 2:152}

def usage():
    print(f"Usage: {__name__} <EXPERIMENT_DIRECTORY>")
    exit()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    # Loads hex mappings
    for m in mapObjects:
        load_mappings("../data/en.csv", mapObjects[m])

    load_similar_mappings("../data/similar/leven.csv", mapObjects["LEVEN"])
    load_similar_mappings("../data/similar/nysiis.csv", mapObjects["NYSIIS"])
    load_similar_mappings("../data/similar/metaphone.csv", mapObjects["METAPHONE"])

    target_dir = sys.argv[1]

    for f in os.listdir(f"{target_dir}"):

        path = target_dir + f

        if f.endswith(".pkl"):
            
            exp = pickle.load(open(path, "rb"))
            
            for a in exp.AttackSchema:

                if a: 
                    target_perms = attackTypes[a[1]]
                    trustwords = a[3]
                    metric = a[0]

                    num_of_perms = num_of_perms_of_words(str(trustwords), mapObjects[metric], PRINT=False)

                    if num_of_perms < target_perms:
                        print(f"[!] Error: file {f} has an invalid attack!")


                    
    

    