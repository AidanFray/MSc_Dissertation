import time

class Experiment:

    def __init__(self, experimentID, userAgent):
        self.ExperimentID = experimentID
        self.VisualWords = []
        self.Responses = []

        # If no attack it will be None
        # Design:
        #
        #   [<SIMILARY_METRIC>, <ATTACK_TYPE>, <SIMILAR_WORDS>]
        #
        self.AttackSchema = []
        self.AudioButtonClicks = []

        self.StartTime = time.time()
        self.RoundStartTimes = []
        self.RoundEndTimes = []
        self.EndTime = None

        self.UserAgent = userAgent

    def add_round(self, visualWords, attackSchema=None):
        self.VisualWords.append(visualWords)
        self.AttackSchema.append(attackSchema)
        self.AudioButtonClicks.append(0)

    def record_response(self, response):
        self.Responses.append(response)

    def record_round_start_time(self):
        self.RoundStartTimes.append(time.time())

    def record_round_end_time(self):
        self.RoundEndTimes.append(time.time())

    def get_round_number(self):
        return len(self.Responses)

    def get_current_wordlist(self):
        return self.VisualWords[-1]

    def get_current_respose(self):
        return self.Responses[-1]

    def get_current_attack_wordlist(self):
        attackSchemea = self.AttackSchema[-1]
        
        # Last value is the wordlist
        return attackSchemea[2]

    def increment_audio_clicks(self):
        self.AudioButtonClicks[-1] += 1

    def is_attack(self):
        return self.AttackSchema[-1]

    def num_of_rounds(self):
        return len(self.Responses)

    def end_experiment(self):
        self.EndTime = time.time()
    
    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(dictionary):
        
        exp = Experiment(None, None)

        exp.ExperimentID        = dictionary["ExperimentID"]
        exp.VisualWords         = dictionary["VisualWords"]
        exp.Responses           = dictionary["Responses"]
        exp.AttackSchema        = dictionary["AttackSchema"]
        exp.AudioButtonClicks   = dictionary["AudioButtonClicks"]
        exp.StartTime           = dictionary["StartTime"]
        exp.RoundStartTimes     = dictionary["RoundStartTimes"]
        exp.RoundEndTimes       = dictionary["RoundEndTimes"]
        exp.EndTime             = dictionary["EndTime"]
        exp.UserAgent           = dictionary["UserAgent"]

        return exp