import sys

def usage():
    print("[!] Usage: ./reduce_complexity <INPUT_DATA_FILE> <OUT_FILENAME>")
    exit()

if len(sys.argv) != 3:
    usage()

input_filename = sys.argv[1]
output_filename = sys.argv[2]

data_occurrence = {}

def count_occurrences():

    # Loads in the data and counts occurrence
    with open(input_filename) as file:

        for line in file:

            try:
                f = float(line.strip())

                if not f in data_occurrence:
                    data_occurrence[f] = 1
                else:
                    data_occurrence[f] += 1
            except ValueError as e:
                print(f"[!] Ignored warning: {e}")

    # Saves the data as the count format
    with open(output_filename, "w") as file:
        for d in data_occurrence:
            file.write(f"{d}: {data_occurrence[d]}\n")


if __name__ == "__main__":
    count_occurrences()