import os
import sys
import hashlib

"""
    Script that is used to create a list of random keys
    for a benchmark
"""

def usage():
    print(f"Usage {__file__} <NUMBER_OF_KEYS>")
    exit()

def gen_hash():
    data = os.urandom(10)
    h = hashlib.md5(data).hexdigest()
    return h[:16]

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        usage()

    num_of_keys = int(sys.argv[1])

    for x in range(num_of_keys):
        print(gen_hash())


    

