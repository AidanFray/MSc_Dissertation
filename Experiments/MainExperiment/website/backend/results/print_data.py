import pickle
import sys; sys.path.insert(0, "..")
import experiment

def line():
    print("#" * 27)

# Printing out FP
def red_text(t):
    return f"\033[1;0;41m{t}\33[0m"

# Printing out FN
def blue_text(t):
    return f"\033[1;0;44m{t}\33[0m"


def print_header(text):

    # Pads text
    while len(text) < 18:
        text += " "

    line()
    print(f"## {text}## [{len(exp.VisualWords)}]")
    line()


def print_numbered_list(list):
    for i, e in enumerate(list):
        print(f"\t{i + 1}. {e}")
    print()

exp = pickle.load(open(f"{sys.argv[1]}", "rb"))

print("Experiment: ")

print_header("Visual Words")
print_numbered_list(exp.VisualWords)

print_header("Responses")
for i, e in enumerate(exp.Responses):

    # Counts errors in the experiment
    if exp.AttackSchema[i] != None and e == "True":
        e = red_text(e)

    elif exp.AttackSchema[i] == None and e == "False":
        e = blue_text(e)

    print(f"\t{i + 1}. {e}")
print()

print_header("Audio Words")
print_numbered_list(exp.AttackSchema)

print_header("Audio Clicks")
for i, e in enumerate(exp.AudioButtonClicks):
    if int(e) > 1:
        e = blue_text(e)
    elif int(e) == 0:
        e = red_text(e)

    print(f"\t{i + 1}. {e}")
print()
    
print_header("Start/End Times")
start   = float(exp.StartTime)
end     = float(exp.EndTime)
print("\n\t" + str(start))
print("\t" + str(end) + '\n')

print_header("Overall Time")
print("\n\t" + str(round(end - start, 2)), "Seconds\n")

print_header("User Agent")
print("\n\t", exp.UserAgent + "\n")
