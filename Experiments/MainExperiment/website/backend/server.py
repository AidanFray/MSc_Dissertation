from flask import Flask, request, send_from_directory, render_template, session
from flask_cors import cross_origin
from pydub import AudioSegment
import random
import pickle
import itertools
import uuid
import time
import os

from CONFIG import BASE_FILE_LOCATION
from experiment import Experiment
import attack
import utils

app = Flask(__name__, static_folder="./build/static", template_folder="./build/")
app.secret_key = "b9d53fe4b4564a95aed2cf966857540d"

WORDLIST_NAME = "trustwords.csv"

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
                words = exp.get_current_attack_wordlist()
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

            if utils.experiment_finished(exp_id):

                exp = Experiment.from_json(session[exp_id])
                exp.end_experiment()
                session[exp_id] = exp.to_json()

                utils.save_experiment(Experiment.from_json(session[exp_id]))

                return "DONE"

            return "  ".join(Experiment.from_json(session[exp_id]).get_current_wordlist())

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

        utils.gen_new_words(WORDLIST)

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
                
                if not utils.experiment_finished(exp_id):
                    utils.gen_new_words(WORDLIST)

                return "OK"
            else:
                return "Error: No experiment found!", 400

        else:
            return "Error: Missing parameter \'result\'", 400

WORDLIST = utils.load_wordlist(f"{BASE_FILE_LOCATION}data/{WORDLIST_NAME}")

if __name__ == "__main__":
    app.run()

