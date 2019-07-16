import sys

sys.path.append("..")

from util import permutations, load
from mappings import Mappings
from util import CONFIG

"""
    Script that tests that the caluclated permutation number
    is correct
"""

metrics = ["soundex"]
size = [1000, 10000, 100000]
staticPositions = [[], [0], [0, 2]]
staticWords = [0, 1, 2]

for m in metrics:

    mappingObj = Mappings()
    load.load_similar_mappings(f"../../data/similar/{m}.csv", mappingObj)
    load.load_mappings("../../data/en.csv", mappingObj)

    for s in size:
        for w in staticWords:

            filePath = f"{m}/{m}-{s}/{m}-static-{w}.txt"

            data = open(filePath, "r").readlines()

            for d in data:
                d = d.strip()
                parts = d.split(" ")

                words = parts[:4]
                target = int(parts[4])

                actual = permutations.similar_perms_size(words, mappingObj, staticPos=staticPositions[w])

                if actual != target and not actual > CONFIG.MAX_PEM_SIZE:
                    print("[!] Non matching perms:")
                    print(" ".join(words))
                    print(f"Metric: {m}")
                    print(f"Actual: {actual} - Expected: {target}")
                    exit()

