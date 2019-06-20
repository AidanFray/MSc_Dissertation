from flask import Flask, request, send_from_directory
from flask_cors import cross_origin
from pydub import AudioSegment
import random
import uuid
import time
import os

import create_custom_audio

######################################
# TODO: Some sort of persistance for 
#       the experiments is needed
######################################

app = Flask(__name__)

experiments = {}

WORDS = ["ABACUS", "ABBREVIATE", "ABIDING", "ADJACENCY"]

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

                words =  experiments[exp_id][0]
                filePath = f"./audio/generated/{'_'.join(words)}.mp3"

                if not os.path.isfile(filePath):

                    combined = AudioSegment.from_mp3(f"audio/{words[0].upper()}.mp3")

                    for w in words[1:]:
                        a = AudioSegment.from_mp3(f"audio/{w.upper()}.mp3")
                        combined += a

                    combined.export(filePath, format="mp3")
                    print("[!] Audio created!")

                print(filePath)
                return send_from_directory('audio/generated', filePath.split("/")[-1])
            else:
                return "Error: No experiment found!"

        else:
            return "Error: Missing parameter \'id\'"

@app.route('/get_words')
@cross_origin()
def get_words():
    
    if request.method == "GET":
        exp_id = request.args.get("id", None)

        if exp_id:
            
            if exp_id in experiments:
                return " ".join(experiments[exp_id][0])
            else:
                return "Error: No experiment found!"

        else:
            return "Error: Missing parameter \'id\'"

@app.route('/new_experiment')
@cross_origin()
def new_experiment():

    # TODO: GET INPUT: Similarity scheme
    similar_scheme = "SOUNDEX"
    exp_id = str(uuid.uuid4())

    # TODO: Load wordlist of server start
    random.shuffle(WORDS)
    words = WORDS[:4]
    
    experiments[exp_id] = [words, similar_scheme]
    
    return exp_id

@app.route('/submit_result')
@cross_origin()
def submit_result():

    # INPUT:
    #   - Response (Accpet/Decline)
    #   - Experiment ID

    # TODO: Should use the response to update the result of the experiment

    return "OK"

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