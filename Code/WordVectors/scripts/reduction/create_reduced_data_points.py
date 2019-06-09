import sys

"""
Script that takes the reduction file and creates a reduced set of values depending on the factor

i.e. 0.1 will produce a set with the proportions of a 10th of a size.
"""

def usage():
    print("[!] Usage: ./create_reduced_data_points.py <INPUT_DICT_FILE> <OUT_FILENAME> <REDUCE_FACTOR (0.0-1.0)")
    exit()

if len(sys.argv) != 4:
    usage()

input_filename = sys.argv[1]
output_filename = sys.argv[2]
reduce_factor = float(sys.argv[3])

# Loads a populates the dictionary
dictionary_data = {}
with open(input_filename) as file:

    for line in file:

        data, occurrence = line.split(":")

        # Add types
        data = float(data)
        occurrence = int(occurrence)

        dictionary_data[data] = occurrence


# Saves the new data points
with open(output_filename, "w") as file:

    for d in dictionary_data:
        string = str(d) + "\n"
        file.write(string * int(dictionary_data[d] * reduce_factor))