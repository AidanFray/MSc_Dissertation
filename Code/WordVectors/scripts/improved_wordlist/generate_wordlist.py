import sys
import dbm

"""
This script uses the database generated from "generate_database.py" to construct the best
wordlist based of the distances of the word vectors
"""


def load_wordlist(fileName):
    """
    Loads a wordlist to memory
    """

    data = []
    with open(fileName) as file:
        
        for line in file:

            # Formats the line
            line = line.strip()
            line = line.upper()

            data.append(line)

    return data

def save_wordlist(fileName, new_wordlist):
    """
    Saves the newly computed words
    """

    with open(fileName, "w") as file:
        for n in new_wordlist:
            file.write(n + "\n")

def best_wordlist_search(word_list, vec_database):
    new_wordlist = []
    new_wordlist_indices = []
    
    print("[*] Searching for the best pair....", end="", flush=True)
    biggest_pair      = None
    biggest_pair_dist = None
    for pair in vec_database.keys():

        dist = float(vec_database[pair])
        if biggest_pair_dist is None or dist > biggest_pair_dist:
            biggest_pair_dist = dist
            biggest_pair = pair

    # Grabs and splits both indices and converts them to integers
    index1, index2 = list(map(int, biggest_pair.decode("utf-8").split("-")))
    new_wordlist_indices =  [index1, index2]
    new_wordlist         =  [word_list[index1], word_list[index2]]
    print("[OK]")

    print("[*] Begining construction of the new wordlist")
    while len(new_wordlist_indices) < new_wordlist_size:

        best_word_index = None
        best_avg_distance = None
        for word_index, candidate_word in enumerate(word_list):
                
            total_distance = 0
            for new_word_index in new_wordlist_indices:

                # Checks for the presence of the value
                if not word_index in new_wordlist_indices:

                    # Words out the alphabetic order
                    word_pair = [
                                    candidate_word, 
                                    word_list[new_word_index]
                                ]
                    word_pair.sort()

                    if word_pair[0] == candidate_word:
                        query = f"{word_index}-{new_word_index}"
                    else:
                        query = f"{new_word_index}-{word_index}"

                    total_distance += float(vec_database[query])

            avg_distance = total_distance / len(new_wordlist_indices)

            # Checks for the best value
            if best_avg_distance == None or avg_distance > best_avg_distance:
                best_word_index = word_index
                best_avg_distance = avg_distance
                best_word = word_list[best_word_index]

        print(f"\tBest word: {best_word}", end=f"{' ' * 20}\r", flush=True)
        new_wordlist_indices.append(best_word_index)
        new_wordlist.append(best_word)

    return new_wordlist

def usage():
    print(f"[!] Usage: ./{__file__} <WORDLIST> <DATABASE> <OUTFILE> <WORDLIST_SIZE>")
    exit()

if __name__ == "__main__":

    # Argument handing
    if len(sys.argv) != 5:
        usage()

    wordlist_path = sys.argv[1]
    database_path = sys.argv[2]
    outfile_path  = sys.argv[3]
    new_wordlist_size = int(sys.argv[4])

    print("[*] Initalisaing data sources....", end="", flush=True)
    wordlist = load_wordlist(wordlist_path)
    vec_database = dbm.open(database_path, "r")
    print("[OK]")

    new_wordlist = best_wordlist_search(wordlist, vec_database)
    save_wordlist(outfile_path, new_wordlist)