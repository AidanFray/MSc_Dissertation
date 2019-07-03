import sys
"""
Script to generate key pairs for trustword combinations
"""

key_pairs = {}

def usage():
    print(f"Usage: ./{__file__} <LIST_OF_FINGERPRINTS>")
    exit()

def load_fingerprints(fingerprints, filepath):
    
    with open(filepath) as file:

        for line in file:
            fingerprints.append(line.strip())

def xor_fingerprint(f1, f2):

    b1 = int(f1, 16)
    b2 = int(f2, 16)

    xor = b1 ^ b2

    return hex(xor)[2:].zfill(40)


def gen_pairs(fingerprints, numOfPairs):

    count = 0
    for i1, f1 in enumerate(fingerprints):
        for _, f2 in enumerate(fingerprints[i1 + 1:]):
            print(xor_fingerprint(f1, f2))

            count += 1

            if count > numOfPairs:
                exit()

if __name__ == "__main__":
    
    NUMBER_OF_PAIRS = 10000

    if len(sys.argv) != 2:
        usage()

    fingerprint_filepath = sys.argv[1]
    
    fingerprints = []
    load_fingerprints(fingerprints, fingerprint_filepath)

    gen_pairs(fingerprints, NUMBER_OF_PAIRS)