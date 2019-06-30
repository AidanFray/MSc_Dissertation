import sys
sys.path.insert(0, ".")
import attack

"""
Script used to show the probabilities of genereating a certain attack
"""

WORDS = ["WORD", "TEST", "WATCH", "COMPUTER"]

METRICS = ["SOUNDEX", "METAPHONE", "NYSIIS"]

METRIC_COUNT = {
    METRICS[0]: 0,
    METRICS[1]: 0,
    METRICS[2]: 0,
}

ATTACK_TYPE_COUNT = {
    0: 0,
    1: 0,
    2: 0,
}

ROUNDS = 1000

def check_attacks():
    for x in range(ROUNDS):
        sys.stderr.write(f"{x}/{ROUNDS}\r")
        sys.stderr.flush()

        a = attack.decision(WORDS)
        if a != None: 
            METRIC_COUNT[a[0]] += 1
            ATTACK_TYPE_COUNT[a[1]] += 1

    # Prints out data
    for c in METRIC_COUNT:
        print(c, METRIC_COUNT[c] / ROUNDS)

    print()

    for a in ATTACK_TYPE_COUNT:
        print(a, ATTACK_TYPE_COUNT[a] / ROUNDS)

if __name__ == "__main__":
    check_attacks()
