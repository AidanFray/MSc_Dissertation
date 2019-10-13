import os
import sys
import pickle

sys.path.append("..")

trick_attacks = {}
all_attacks = {}

def usage():
    print(f"Usage: python {__name__} <TARGET_DIR>")
    exit()

def checkAudioClicks(exp):

    missedCount = 0
    for i, e in enumerate(exp.AudioButtonClicks):
        if int(e) == 0:
            missedCount += 1

    return missedCount




if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        usage()

    target_dir = sys.argv[1]
    

    for file in os.listdir(f"{target_dir}"):
        if file.endswith(".pkl"):
            
            f = target_dir + file

            exp = pickle.load(open(f, "rb"))

            missedCount = checkAudioClicks(exp)

            if missedCount > 2:
                print(f"[!] {file} Has rounds with no AudioButtons clicks: {missedCount} ")