import sys
import base64
from Crypto.Hash import SHA1


sys.path.insert(0, "..")

from util.trustwords import *

def PGP_key_hash(key_data):
    # Skips headers and formatting lines
    key_base64 = ""
    for l in key_data[1:-2]:
        key_base64 += l.strip()

    # All the bytes from the key
    key_bytes = base64.b64decode(key_base64)

    # Takes the PGP packey length from the header
    key_length = int.from_bytes(key_bytes[1:3], byteorder="big")

    # Takes the header and length
    key_formatted_bytes = key_bytes[:key_length + 3]

    sha1 = SHA1.new()
    sha1.update(key_formatted_bytes)

    # Takes the left 64-bit
    return sha1.hexdigest()[:16].upper()

def generate_words_for_PGP_keys(key_path_1, key_path_2, mapping):
    
    key_data_1 = []
    with open(key_path_1) as key1:
        key_data_1 = key1.readlines()
    
    key_data_2 = []
    with open(key_path_2) as key2:
        key_data_2 = key2.readlines()

    # Takes the left 64-bit
    key_finger_print_1 = PGP_key_hash(key_data_1)
    key_finger_print_2 = PGP_key_hash(key_data_2)

    combined_key = XOR_fingerprints(key_finger_print_1, key_finger_print_2)
    fingerprint_to_words(combined_key, mapping)
