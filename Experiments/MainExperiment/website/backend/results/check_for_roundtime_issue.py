import os
import sys
import pickle

sys.path.append("..")

trick_attacks = {}
all_attacks = {}

for file in os.listdir("."):
    if file.endswith(".pkl"):
        
        exp = pickle.load(open(file, "rb"))

        if len(exp.RoundStartTimes) != len(exp.RoundEndTimes):
            print(f"[!] {file} has issues with Round times!")