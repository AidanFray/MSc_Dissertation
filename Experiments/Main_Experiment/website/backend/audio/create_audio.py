import sys
from gtts import gTTS
import time
import os

"""
    Script that generates .mp3 files for each words pronunciation
"""

def usage():
    print(f"Usage: ./{__file__} <WORDLIST>")
    exit()

def save_word(word):
    tts = gTTS(text=word, lang='en')
    tts.save(f"{word}.mp3")

def check_for_previous_runs(words):

    pos = 0

    for w in words:
        if not os.path.exists(f"./{w}.mp3"):
            return pos

        pos += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    wordlist_path = sys.argv[1]

    words = []
    with open(wordlist_path) as file:
        words = file.readlines()

    words = list(map(str.strip, words))

    previous_run = check_for_previous_runs(words)
    print(f"[!] Continuing from position: {previous_run} ({words[previous_run]})")

    for index, w in enumerate(words[previous_run:]):
        start_time = time.time()
        save_word(w)
        end_time = time.time()

        overall_time = ((end_time - start_time) * len(words) - index + previous_run) / 3600

        print(f"[!] {index + previous_run}/{len(words)} -- Time: {round(overall_time, 2)} Hours", end="\r", flush=True)
