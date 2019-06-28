from flask import Flask, request, send_from_directory, render_template, session
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
app.secret_key = "b9d53fe4b4564a95aed2cf966857540d"

# This needs changing on the PythonAnywhere site
#
#   /home/AFray/website/
#
BASE_FILE_LOCATION = ""

WORDLIST_NAME       = "trustwords.csv"
SIMILAR_WORDS_FILE  = "en_soundex.csv"

# SIMILARITY_METRICS  = "SOUNDEX"

NUMBER_OF_ROUNDS = 15
ATTACK_CHANCE = 0.25

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

    """
    Gets the currently active audio file
    """

    if request.method == "GET":

        exp_id = session.get("exp_id")

        if exp_id in session:

            # Converts the session cookie to object
            exp = Experiment.from_json(session[exp_id])

            # Increments and saves changes
            exp.increment_audio_clicks()
            session[exp_id] = exp.to_json()

            # Checks for an attack case
            if exp.is_attack():
                words = exp.get_current_audio_wordlist()
            else:
                words = exp.get_current_wordlist()
            
            filePath = f"{BASE_FILE_LOCATION}audio/generated/{'_'.join(words)}.mp3"
            if not os.path.isfile(filePath):

                combined = AudioSegment.from_mp3(f"{BASE_FILE_LOCATION}audio/{words[0].upper()}.mp3")

                for w in words[1:]:
                    a = AudioSegment.from_mp3(f"{BASE_FILE_LOCATION}audio/{w.upper()}.mp3")
                    combined += a

                combined.export(filePath, format="mp3")

            return send_from_directory(f'{BASE_FILE_LOCATION}audio/generated', filePath.split("/")[-1])
        
        return "No Experiment found", 400

@app.route('/get_words')
@cross_origin()
def get_words():
    """
    Gets the currently active set of words
    """

    if request.method == "GET":
        exp_id = session.get("exp_id")

        if exp_id in session:

            if experiment_finished(exp_id):

                exp = Experiment.from_json(session[exp_id])
                exp.end_experiment()
                session[exp_id] = exp.to_json()

                save_experiment(Experiment.from_json(session[exp_id]))

                return "DONE"

            return " ".join(Experiment.from_json(session[exp_id]).get_current_wordlist())

        else:
            return "Error: Experiment ID not found", 400

    return "Error: Method not allowed", 400

@app.route("/get_id")
@cross_origin()
def get_id():
    return session.get("exp_id")

@app.route('/new_experiment')
@cross_origin()
def new_experiment():
    """
    This end point is designed to initialise the experiment attached to a certain ID
    """

    if not session.get("exp_id"):

        user_agent = request.headers.get("User-Agent")

        exp_id = str(uuid.uuid4())

        session['exp_id'] = exp_id
        session[exp_id] = Experiment(exp_id, user_agent).to_json()

        gen_new_words()

        return exp_id

    return session.get('exp_id')

@app.route('/submit_result')
@cross_origin()
def submit_result():

    if request.method == "GET":
        result = request.args.get("result", None)

        if result:

            exp_id = session.get("exp_id")
            
            if exp_id in session:

                exp = Experiment.from_json(session[exp_id])
                exp.record_response(result)
                session[exp_id] = exp.to_json()
                
                if not experiment_finished(exp_id):
                    gen_new_words()

                return "OK"
            else:
                return "Error: No experiment found!", 400

        else:
            return "Error: Missing parameter \'result\'", 400

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

    if len(wordlist) == 0:
        raise Exception("No word list loaded!")

    return wordlist

def load_similar_words(path):
    similar_words = {}

    with open(path, "r") as file:

        for line in file:
            line = line.strip()
            line_parts = line.split(",")

            similar_words[line_parts[0]] = line_parts[1:-1]

    return similar_words 

def gen_new_words():
    
    """
    This method provides the next round of words, it is responsible for dealing 
    out the 'attack' cases and working out their matches
    """

    exp_id = session.get("exp_id")

    new_words = get_random_words()

    # # Determines if their is an attack
    audio_words = None
    if random.random() < ATTACK_CHANCE:
        audio_words = generate_similar_match(new_words)

    exp = Experiment.from_json(session[exp_id])
    exp.add_round(new_words, audio_words)
    session[exp_id] = exp.to_json()

def get_random_words():
    random.shuffle(WORDS)
    return WORDS[:4]

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

def experiment_finished(exp_id):
    return Experiment.from_json(session[exp_id]).num_of_rounds() >= NUMBER_OF_ROUNDS

SIMILAR_WORDS = load_similar_words(f"{BASE_FILE_LOCATION}data/similar/{SIMILAR_WORDS_FILE}")
WORDS = load_wordlist(f"{BASE_FILE_LOCATION}data/{WORDLIST_NAME}")

if __name__ == "__main__":
    app.run(threaded=True)

