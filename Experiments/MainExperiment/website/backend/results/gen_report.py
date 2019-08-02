import os
import pickle
import sys; sys.path.insert(0, "..")
import experiment

def usage():
    print(f"Usage: python {__name__} <OUTPUT_FILE_NAME>")
    exit()

# Printing out FP
def red_text(t):
    return f"\033[1;0;41m{t}\33[0m"

# Printing out FN
def blue_text(t):
    return f"\033[1;0;44m{t}\33[0m"

def findSuccessfulAttacks(exp):


    attacks = []
    for i, e in enumerate(exp.Responses):

        # Counts errors in the experiment
        if exp.AttackSchema[i] != None and e == "True":
            attacks.append("\t" + str(exp.AttackSchema[i]))

    return attacks

def checkAudioClicks(exp):

    missedCount = 0
    for i, e in enumerate(exp.AudioButtonClicks):
        if int(e) == 0:
            missedCount += 1

    if missedCount > 5:
        return True
    else:
        return False

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    outputFileName = sys.argv[1]

    for file in os.listdir("."):
        if file.endswith(".pkl"):

            exp = pickle.load(open(file, "rb"))
            print(f"-------------------- {file} --------------------")

            if checkAudioClicks(exp):
                print("#####################################")
                print("!! Possible click-through detected !!")
                print("#####################################")
                print()

            # User-agent
            print("## User-agent ##: \n")
            print("\t", exp.UserAgent)
            print()

            # Successfull attacks
            attacks = findSuccessfulAttacks(exp)

            if len(attacks) > 1:
                print("## Successfull attacks ##:\n")
                for a in attacks:
                    print(a)
            else:
                print("## No attacks ##\n")
                

            print("\n\n")


            # os.system(f"echo -------------------- {file} -------------------- >> {outputFileName}")
            # os.system(f"python3 print_data.py {file} 2>&1 | tee -a {outputFileName}")