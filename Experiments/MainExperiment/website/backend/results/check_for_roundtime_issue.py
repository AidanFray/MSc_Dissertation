import os
import sys
import pickle

sys.path.append("..")

trick_attacks = {}
all_attacks = {}

def usage():
    print(f"Usage: python {__name__} <TARGET_DIR>")
    exit()


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        usage()

    target_dir = sys.argv[1]


    for file in os.listdir(f"{target_dir}"):
        if file.endswith(".pkl"):
            
            f = target_dir + file

            exp = pickle.load(open(f, "rb"))

            if len(exp.RoundStartTimes) != len(exp.RoundEndTimes):
                print(f"[!] {file} has issues with Round times!")