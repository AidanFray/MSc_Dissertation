from flask import session
from experiment import Experiment
import pickle
import attack
import random

from CONFIG import BASE_FILE_LOCATION, NUMBER_OF_ROUNDS, GRACE_ROUNDS

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

def gen_new_words(wordlist):
    
    """
    This method provides the next round of words, it is responsible for dealing 
    out the 'attack' cases and working out their matches
    """

    exp_id = session.get("exp_id")
    exp = Experiment.from_json(session[exp_id])

    if exp.get_round_number () >= GRACE_ROUNDS:
        # # Determines if their is an attack
        attack_schema = attack.decision()
    else:
        attack_schema = None

    if attack_schema:

        # Grabs the original words to show
        new_words = attack_schema[3]
    else:
        new_words = get_random_words(wordlist)

    exp = Experiment.from_json(session[exp_id])
    exp.add_round(new_words, attack_schema)
    session[exp_id] = exp.to_json()

def get_random_words(wordlist):
    random.shuffle(wordlist)
    return wordlist[:4]

def experiment_finished(exp_id):
    return Experiment.from_json(session[exp_id]).num_of_rounds() >= NUMBER_OF_ROUNDS
