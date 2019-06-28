from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import urllib.request as url
import urllib
import time
import json
import sys
import os

driver = webdriver.Firefox()
driver.get("https://api.forvo.com/demo/")

def load_wordlist(filepath):
    words = []
    with open(filepath) as file:
        words = file.readlines()

    words = list(map(str.strip, words))
    return words

def get_response(word):
    word_textbox = driver.find_element_by_id("word")

    word_textbox.clear()
    word_textbox.send_keys(word)
    word_textbox.send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div[2]/div/section/div/div/pre"))
        )
    except:
        print(f"[!] Error waiting for respose for word: {word}")
        print("[!] Continuing...")
        return

    RESPONSE = False
    
    # Need to URL ENCODE THIS 
    while not RESPONSE:
        link = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section/div/a")
        if urllib.parse.quote_plus(word) in link.text: 
            RESPONSE = True
        else:
            time.sleep(0.5)

    response = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section/div/div/pre")
    j = json.loads(response.text)

    os.system(f"mkdir words/{word}")
    os.system(f"touch words/{word}/.gitkeep")

    for i in j['items']:
        if i['langname'] == "English":
            url.urlretrieve(i['pathmp3'], f"words/{word}/{word}_{i['sex']}_{i['num_positive_votes']}.mp3")

def check_for_previous_runs(words):

    pos = 0

    for w in words:
        if not os.path.exists(f"words/{w}"):
            return pos

        pos += 1

def usage():
    print(f"[!] Usage: ./{__file__} <WORDLIST_PATH>")
    exit()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    wordlist_path = sys.argv[1]

    print("[!] Loading wordlist...", end="", flush=True)
    WORDS = load_wordlist(wordlist_path)
    print("[OK]")

    previous_position = check_for_previous_runs(WORDS) - 1
    print(f"[!] Starting program from previous position: {previous_position}")

    for i, w in enumerate(WORDS[previous_position:]):
        get_response(w)
        print(f"[*] Word: {i + previous_position}/{len(WORDS)}", end="\r", flush=True)

