import time

class Experiment:

    def __init__(self, experimentID, userAgent):
        self.ExperimentID = experimentID
        self.VisualWords = []
        self.Responses = []

        # If they're the same as the VisualWords they will be blank
        self.AudioWords = []

        self.StartTime = time.time()
        self.EndTime = None

        self.UserAgent = userAgent

    def add_round(self, visualWords, audioWords=None):
        self.VisualWords.append(visualWords)
        self.AudioWords.append(audioWords)

    def record_response(self, response):
        self.Responses.append(response)

    def get_current_wordlist(self):
        return self.VisualWords[-1]

    def get_current_respose(self):
        return self.Responses[-1]

    def get_current_audio_wordlist(self):
        return self.AudioWords[-1]

    def is_attack(self):
        return self.AudioWords[-1]

    def num_of_rounds(self):
        return len(self.Responses)

    def end_experiment(self):
        self.EndTime = time.time()
    
    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(dictionary):
        
        exp = Experiment(None, None)

        exp.ExperimentID    = dictionary["ExperimentID"]
        exp.VisualWords     = dictionary["VisualWords"]
        exp.Responses       = dictionary["Responses"]
        exp.AudioWords      = dictionary["AudioWords"]
        exp.StartTime       = dictionary["StartTime"]
        exp.EndTime         = dictionary["EndTime"]
        exp.UserAgent       = dictionary["UserAgent"]

        return exp