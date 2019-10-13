import csv

def load(filePath):

    data = []
    with open(filePath) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row)

    return data

def save(filePath, data):

    with open(filePath, "w") as file:

        for d in data:
            file.write(",".join(d) + "\n")

def usage():
    print(f"Usage: ./{__name__} <MAIN_WORKER_FILE> <HIT_WORKER_FILE>")
    exit()