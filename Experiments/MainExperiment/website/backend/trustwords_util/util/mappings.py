from copy import deepcopy

class MappingModes():
    HexToWord = 0
    WordToHex = 1
    SimilarWord = 2

class Mappings:

    def __init__(self):
        super()

        self._hex_to_word_mapping = {}
        self._word_to_hex_mapping = {}
        self._similar_word_mapping = {} 

        self._mappings = [
            self._hex_to_word_mapping,
            self._word_to_hex_mapping,
            self._similar_word_mapping
        ]

    def getMapping(self, mode, query):
        
        # Checks for an empty list
        if len(self._mappings[mode]) == 0:
            raise Exception(f"Error: {mode} not loaded")

        output = self._mappings[mode][query]

        # Copy is required to make sure the values remian read only
        if isinstance(output, list):
            return output.copy()
        else:
            return output

