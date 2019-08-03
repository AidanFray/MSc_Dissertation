import os
import pickle
import sys; sys.path.insert(0, "..")
import experiment

def usage():
    print(f"Usage: python {__name__} <TARGET_DIR>")
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

def findFalsePositives(exp):
    fp = []
    for i, e in enumerate(exp.Responses):

        # Counts errors in the experiment
        if exp.AttackSchema[i] == None and e == "False":
            attacks.append("\t" + str(exp.AttackSchema[i]))

    return fp

def checkForHighSpeed(exp):
    
    # If done quicker than 5 minutes
    if getExperimentSpeed(exp) < 200:
        return True
    else:
        return False

def checkAudioClicks(exp):

    missedCount = 0
    for i, e in enumerate(exp.AudioButtonClicks):
        if int(e) == 0:
            missedCount += 1

    if missedCount > 5:
        return True
    else:
        return False

def getExperimentSpeed(exp):

    start   = float(exp.StartTime)
    end     = float(exp.EndTime)

    return end - start

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    target_dir = sys.argv[1]

    for f in os.listdir(f"{target_dir}"):

        path = target_dir + f

        if f.endswith(".pkl"):

            exp = pickle.load(open(path, "rb"))
            print(f"-------------------- {f} --------------------")

            if checkAudioClicks(exp):
                print()
                print("\t           Click-through detected      ")
                print()
                break

            if checkForHighSpeed(exp):
                print(f"!! User was very quick: {round(getExperimentSpeed(exp))} seconds !!")
                print()

            # Successfull attacks
            attacks = findSuccessfulAttacks(exp)

            if len(attacks) > 1:
                print("-- Successfull attacks --\n")
                for a in attacks:
                    print(a)
                print()
            else:
                print("-- No attacks --")


            fp = findFalsePositives(exp)

            if len(fp) > 1:
                print("-- False positives -- : \n")
                for f in fp:
                    print(f)
            else:
                print("-- No false positives --")
            
                
            # User-agent
            print("-- UserAgent -- \n")
            print("\t", exp.UserAgent[:50], "...")
            print()

            print("\n\n")


            # os.system(f"echo -------------------- {file} -------------------- >> {outputFileName}")
            # os.system(f"python3 print_data.py {file} 2>&1 | tee -a {outputFileName}")