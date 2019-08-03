import os
import sys
import pickle

sys.path.append("..")

trick_attacks = {}
all_attacks = {}

def checkAudioClicks(exp):

    missedCount = 0
    for i, e in enumerate(exp.AudioButtonClicks):
        if int(e) == 0:
            missedCount += 1

    return missedCount

for file in os.listdir("."):
    if file.endswith(".pkl"):
        
        exp = pickle.load(open(file, "rb"))

        missedCount = checkAudioClicks(exp)

        if missedCount > 2:
            print(f"[!] {file} Has rounds with no AudioButtons clicks: {missedCount} ")