class MappingModes():
    HexToWord = 0
    WordToHex = 1
    SimilarWord = 2

class Mappings:

    _hex_to_word_mapping = {}
    _word_to_hex_mapping = {}
    _similar_word_mapping = {} 

    _mappings = [
        _hex_to_word_mapping,
        _word_to_hex_mapping,
        _similar_word_mapping
    ]

    def getMapping(self, mode, query):
        return self._mappings[mode][query]

