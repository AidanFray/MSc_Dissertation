import sys
import random

def usage():
    print(f"Usage: python ./{__file__} <WORDLIST> <NUM_OF_MATCHES>")
    exit()

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        usage()

    wordlist_path = sys.argv[1]
    num_of_matches = int(sys.argv[2])

    wordlist = []
    with open(wordlist_path) as file:
        wordlist = file.readlines()
        wordlist = list(map(str.strip, wordlist))

    for x in range(num_of_matches):
        word1 = wordlist[random.randint(0, len(wordlist) - 1)]
        word2 = wordlist[random.randint(0, len(wordlist) - 1)]

        print(f"{word1}-{word2},")


