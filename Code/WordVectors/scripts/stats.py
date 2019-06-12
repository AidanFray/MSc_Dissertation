import sys
import numpy as np
from scipy import stats

def usage():
    print("[!] Usage: ./stats.py <VALUES.DAT>")
    exit(0)

def load_data(fileName):
    
    data = []
    with open(fileName) as file:
        for line in file:
            data.append(float(line.strip()))

    return data

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        usage()

    data = load_data(sys.argv[1])

    print("###### STATS ######")
    print(f"[!] Mean:   {round(np.average(data), 3)}")
    print(f"[!] Median: {round(np.median(data), 3)}")
    print(f"[!] Max:    {np.max(data)}")
    print(f"[!] Min:    {np.min(data)}")
    print("###################")


