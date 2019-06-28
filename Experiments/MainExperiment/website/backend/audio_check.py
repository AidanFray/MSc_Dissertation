import sys
import os

"""
Script used to check all audio files exist
"""

def usage():
    print(f"python {__file__} <WORDLIST>")
    exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    wordlist_path = sys.argv[1]

    words = []
    with open(wordlist_path) as file:
        for line in file:
            words.append(line.strip())

    for w in words:
        if not os.path.isfile(f"./audio/{w}.mp3"):
            print(f"[!] Missing: {w}!")