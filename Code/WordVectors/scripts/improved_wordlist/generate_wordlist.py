import sys
import dbm

def usage():
    print(f"[!] Usage: ./{__file__} <WORDLIST> <DATABASE> <OUTFILE> <WORDLIST_SIZE>")
    exit()

def load_wordlist(fileName):
    """
    Loads a wordlist to file
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

if __name__ == "__main__":

    if len(sys.argv) != 5:
        usage()

    wordlist_path = sys.argv[1]
    database_path = sys.argv[2]
    outfile_path  = sys.argv[3]
    new_wordlist_size = int(sys.argv[4])

    print("[*] Initalisaing data sources....", end="", flush=True)
    word_list = load_wordlist(wordlist_path)
    vec_database = dbm.open(database_path, "r")
    print("[OK]")

    print("[*] Searching for the best pair....", end="", flush=True)
    biggest_pair      = None
    biggest_pair_dist = None
    for pair in vec_database.keys():

        dist = vec_database[pair]
        if biggest_pair_dist is None or dist > biggest_pair_dist:
            biggest_pair_dist = dist
            biggest_pair = pair

    new_wordlist = []
    new_wordlist += biggest_pair.decode("utf-8").split("-")
    print("[OK]")

    print("[*] Begining construction of the new wordlist")
    while len(new_wordlist) < new_wordlist_size:

        best_word = None
        best_avg_distance = None
        for word in word_list:
                
            total_distance = 0
            for w in new_wordlist:

                if not word in new_wordlist:

                    # Creates the ordered pair ID string
                    word_pair = [word, w]
                    word_pair.sort()

                    total_distance += float(vec_database[f"{word_pair[0]}-{word_pair[1]}"])

            avg_distance = total_distance / len(new_wordlist)

            # Checks for the best value
            if best_avg_distance == None or avg_distance > best_avg_distance:
                best_word = word
                best_avg_distance = avg_distance

        print(f"\tBest word: {best_word}", end=f"{' ' * 20}\r", flush=True)
        new_wordlist.append(best_word)

    save_wordlist(outfile_path, new_wordlist)