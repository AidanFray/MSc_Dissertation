
import sys

sys.path.insert(0, " ..")

from util.trustwords import *
from util.permutations import *

def create_actual_fingerprint_and_key(number_of_words, uncontrolledFingerprint, mapping, gpg):
    
    biggest_perm_size = 0
    biggest_key = None

    DEBUG_FINGERPRINT = None

    # TODO: Determine number of keys to test
    total_keys = 100

    loop = 0
    for x in range(total_keys):
    
        input_data = gpg.gen_key_input(key_type='RSA', key_length=1024, passphrase="1234")
        key = gpg.gen_key(input_data)
        fp = key.fingerprint

        number_finger_chars = int(number_of_words * 4)
        reduced_fingerprint = fp[-number_finger_chars:]

        combined_fingerprint = XOR_fingerprints(reduced_fingerprint, uncontrolledFingerprint)
        trustWords = fingerprint_to_words(combined_fingerprint, mapping, PRINT=False)

        combinations = similar_combinations(trustWords, mapping)
        perm_size = get_perm_size(combinations)

        if perm_size > biggest_perm_size:
            biggest_key = key
            biggest_perm_size = perm_size
            DEBUG_FINGERPRINT = fp

        loop += 1

        print(f"{loop}/{total_keys} Keys complete", end="\r")

    print()
    print(biggest_perm_size)
    print(gpg.export_keys(biggest_key))
    print(DEBUG_FINGERPRINT)

    # TODO: Fix private key export
    print(gpg.export_keys(biggest_key, secret=True))
    