import subprocess
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Usage: ./text_to_memmap.py <INPUT_FILE> <OUTPUT_FILE>")
    exit()

input_filepath = sys.argv[1]
output_filepath = sys.argv[2]

number_of_lines = subprocess.check_output(["wc", "-l", input_filepath]).decode("utf-8")
number_of_lines = int(number_of_lines.split(" ")[0]) + 1

mem = np.memmap(output_filepath, dtype="float32", mode="w+", shape=(1, number_of_lines))

with open(input_filepath, "r") as file:

    index = 0
    for line in file:

        try:
            f = float(line)
            mem[0, index] = f
            index += 1
        except ValueError:
            pass
    
print("[!] Complete!")