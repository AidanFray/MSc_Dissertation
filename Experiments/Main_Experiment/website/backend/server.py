from flask import Flask, request, send_from_directory, render_template
from flask_cors import cross_origin
from pydub import AudioSegment
import random
import pickle
import itertools
import uuid
import time
import os

from experiment import Experiment

app = Flask(__name__, static_folder="./build/static", template_folder="./build/")

SIMILAR_WORDS = {}
WORDLIST = {}

# Format:
#   Similarity   : [None,   'Soundex',  ...]
#   Words tested : [WList1, WList2,     ...]
#   Responses    : [R1,     R2,         ...]
#   Attack match : [[]],  WordList,       ...]
experiments = {}

WORDS = ["ABACUS", "ABBREVIATE", "ABIDING", "ADJACENCY"]
SIMILARITY_METRICS = "SOUNDEX"

NUMBER_OF_ROUNDS = 5
ATTACK_CHANCE = 0.25

# This needs changing on the PythonAnywhere site
#
#   /home/AFray/website/
#
BASE_FILE_LOCATION = ""

def get_random_words():
    random.shuffle(WORDS)
    return WORDS[:4]

# This is used to fix Flask's compatability with the react-routing 
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_audio')
@cross_origin()
def get_audio():

     if request.method == "GET":
        exp_id = request.args.get("id", None)

        if exp_id:
            
            if exp_id in experiments:

                # Checks for an attack case
                if experiments[exp_id].is_attack():
                    words = experiments[exp_id].get_current_audio_wordlist()
                else:
                    words = experiments[exp_id].get_current_wordlist()
                
                filePath = f"{BASE_FILE_LOCATION}audio/generated/{'_'.join(words)}.mp3"

                if not os.path.isfile(filePath):

                    combined = AudioSegment.from_mp3(f"{BASE_FILE_LOCATION}audio/{words[0].upper()}.mp3")

                    for w in words[1:]:
                        a = AudioSegment.from_mp3(f"{BASE_FILE_LOCATION}audio/{w.upper()}.mp3")
                        combined += a

                    combined.export(filePath, format="mp3")

                return send_from_directory(f'{BASE_FILE_LOCATION}audio/generated', filePath.split("/")[-1])
            else:
                return "Error: No experiment found!"

        else:
            return "Error: Missing parameter \'id\'"

@app.route('/get_words')
@cross_origin()
def get_words():
    
    """
    This method provides the next round of words, it is responsible for dealing 
    out the 'attack' cases and working out their matches
    """

    if request.method == "GET":
        exp_id = request.args.get("id", None)

        if exp_id:
            
            if exp_id in experiments:

                # Finishes the experiment
                if experiments[exp_id].num_of_rounds() >= NUMBER_OF_ROUNDS:

                    experiments[exp_id].end_experiment()
                    save_experiment(experiments[exp_id])

                    return "DONE"

                new_words = get_random_words()

                # TODO: Active attack when all word recordsing are avaliable
                # # Determines if their is an attack
                audio_words = None
                # if random.random() < ATTACK_CHANCE:
                #     audio_words = generate_similar_match(new_words)

                experiments[exp_id].add_round(new_words, audio_words)

                return " ".join(new_words)
            else:
                return "Error: No experiment found!"

        else:
            return "Error: Missing parameter \'id\'"

@app.route('/new_experiment')
@cross_origin()
def new_experiment():
    """
    This end point is designed to initialise the experiment attached to a certain ID
    """

    user_agent = request.headers.get("User-Agent")

    exp_id = str(uuid.uuid4())
    experiments[exp_id] = Experiment(exp_id, user_agent)

    return exp_id

@app.route('/submit_result')
@cross_origin()
def submit_result():

    if request.method == "GET":
        exp_id = request.args.get("id", None)
        result = request.args.get("result", None)

        if exp_id and result:
            
            if exp_id in experiments:
                
                experiments[exp_id].record_response(result)

                return "OK"
            else:
                return "Error: No experiment found!"

        else:
            return "Error: Missing parameter \'id\' or \'result\'"

######################
##      UTILS       ##
######################

def save_experiment(expr):
    pickle.dump(expr, open(f"{BASE_FILE_LOCATION}results/{expr.ExperimentID}.pkl", "wb"))

def load_wordlist(path):
    wordlist = []

    with open(path, "r") as file:
        
        for line in file:
            line = line.strip()
            wordlist.append(line)

    return wordlist

def load_similar_words(path):
    similar_words = {}

    with open(path, "r") as file:

        for line in file:
            line = line.strip()
            line_parts = line.split(",")

            similar_words[line_parts[0]] = line_parts[1:-1]

    return similar_words 

def generate_similar_match(wordlist):

    # To make sure permutations size don't get too big    
    MAX_SIMILAR_PERM_SIZE = 100

    combinations = []

    for w in wordlist:

        similar_words = [SIMILAR_WORDS[w]]

        # This is the make sure the cap isn't bias
        if len(similar_words) > MAX_SIMILAR_PERM_SIZE:
            random.shuffle(similar_words)

        combinations += similar_words[:MAX_SIMILAR_PERM_SIZE] 

    perms = list(itertools.product(combinations[0], combinations[1], combinations[2], combinations[3]))

    random_match = list(perms[random.randint(0, len(perms))])
    return random_match

if __name__ == "__main__":

    WORDLIST = load_wordlist(f"{BASE_FILE_LOCATION}data/trustwords.csv")

    #TODO Make this dynamic for the similar metric
    SIMILAR_WORDS = load_similar_words(f"{BASE_FILE_LOCATION}data/similar/en_soundex.csv")

    app.run()