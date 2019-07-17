import re
import sys

sys.path.insert(0, "..")

from .mappings import *

def fingerprint_to_words(fingerprint, mapping, PRINT=True):
    """
    Maps the hex value of the key to a word defined in
    the dictionary loaded
    """

    fingerprint = fingerprint.replace(" ", "")

    trustwords = []

    chunks = re.findall(".{4}", fingerprint)

    for chunk in chunks:
        word = mapping.getMapping(MappingModes.HexToWord, chunk.lower())
        trustwords.append(word)

    if PRINT:

        trustwords_str = " ".join(trustwords)

        print("#" * (len(trustwords_str) + 1))
        print(trustwords_str)
        print("#" * (len(trustwords_str) + 1))

    return trustwords

def XOR_fingerprints(fingerprint1, fingerprint2):
    """
    XORs two fingerprints, this is usefull because pEp
    creates a joint fingerprint from the two parties
    by XORing each parties key
    """

    fingerprint1 = fingerprint1.replace(" ", "")
    fingerprint2 = fingerprint2.replace(" ", "")

    fingerprint_1_parts = re.findall(r".{4}", fingerprint1)
    fingerprint_2_parts = re.findall(r".{4}", fingerprint2)

    combined = []

    for index, value in enumerate(fingerprint_1_parts):
        
        # Parses hex strings to values
        f1 = int(value, 16)
        f2 = int(fingerprint_2_parts[index], 16)

        c = f1 ^ f2

        c_hex = hex(c)[2:].zfill(4)

        combined.append(c_hex)

    return "".join(combined)
