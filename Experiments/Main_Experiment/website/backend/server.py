from flask import Flask, request, send_from_directory
from flask_cors import cross_origin
from pydub import AudioSegment
import random
import uuid
import time
import os

from experiment import Experiment

import create_custom_audio

######################################
# TODO: Some sort of persistance for 
#       the experiments is needed
######################################

app = Flask(__name__)


# Format:
#   Similarity   : [None,   'Soundex',  ...]
#   Words tested : [WList1, WList2,     ...]
#   Responses    : [R1,     R2,         ...]
#   Attack match : [[]],  WordList,       ...]
experiments = {}

WORDS = ["ABACUS", "ABBREVIATE", "ABIDING", "ADJACENCY"]
SIMILARITY_METRICS = "SOUNDEX"

def get_random_words():
    random.shuffle(WORDS)
    return WORDS[:4]

@app.route('/')
def index():
    return "index"

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
                
                filePath = f"./audio/generated/{'_'.join(words)}.mp3"

                if not os.path.isfile(filePath):

                    combined = AudioSegment.from_mp3(f"audio/{words[0].upper()}.mp3")

                    for w in words[1:]:
                        a = AudioSegment.from_mp3(f"audio/{w.upper()}.mp3")
                        combined += a

                    combined.export(filePath, format="mp3")

                return send_from_directory('audio/generated', filePath.split("/")[-1])
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

                new_words = get_random_words()


                # TODO: Randomly choose attack case here with predefined metric
                # TODO: If attack is active generate a list that will be used to create the audio
                audio_words = None

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

    exp_id = str(uuid.uuid4())
    experiments[exp_id] = Experiment()

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

@app.route('/debug')
@cross_origin()
def debug():
    if request.method == "GET":
        debug = request.args.get("debug", None)
        if debug:
            print(debug)
            return debug        
        else:
            print("No places provided")
            return "No places provided"

if __name__ == "__main__":
    app.run()