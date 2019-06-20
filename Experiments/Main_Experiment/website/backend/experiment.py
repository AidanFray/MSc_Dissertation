class Experiment:

    def __init__(self):
        self.VisualWords = []
        self.Responses = []

        # If they're the same as the VisualWords they will be blank
        self.AudioWords = []

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