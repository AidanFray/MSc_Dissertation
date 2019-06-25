import pickle
import sys; sys.path.insert(0, "..")
import experiment


exp = pickle.load(open(f"{sys.argv[1]}", "rb"))

print("Experiment: ")

print("\n## Visual Words ##")
print(exp.VisualWords)

print("\n## Responses ##")
print(exp.Responses)

print("\n## Audio Words ##")
print(exp.AudioWords)

print("\n## Start and End Times ##")
start   = float(exp.StartTime)
end     = float(exp.EndTime)

print(start)
print(end)

print("\n## Overall Time ##")
print(round(end - start, 2), "Seconds")


print("\n## User Agent ##")
print(exp.UserAgent)