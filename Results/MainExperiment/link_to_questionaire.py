import sys
import csv
import os

def usage():
    print(f"Usage: {__name__} <QUESTIONAIRE_PATH> <BATCH_PATH> <DIRECTORY>")
    exit()


def load(filePath):

    data = []
    with open(filePath) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row)

    return data


workers = {}

if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        usage()

    questionaire_path   = sys.argv[1]
    batch_path          = sys.argv[2]
    target_dir          = sys.argv[3]

    # Load batch and link WorkerID to GUID
    batch_data_raw = load(batch_path)

    workerId_index = batch_data_raw[0].index("WorkerId")
    guid_index = batch_data_raw[0].index("Answer.surveycode")

    for row in batch_data_raw[1:]:
        workers.update({row[guid_index]: row[workerId_index]})

    # Uses GUID in directory to get Worker ID that then checks English comprehension
    
    guids = []
    for f in os.listdir(f"{target_dir}"):

        path = target_dir + f

        if f.endswith(".pkl"):

            parts = f.split(".")

            guids.append(parts[0])

    # Loads questionair data
    questionaire_data_raw = load(questionaire_path)

    quest_workerID_index = questionaire_data_raw[0].index("Worker ID")
    quest_english_comp = questionaire_data_raw[0].index("English comprehension")

    for g in guids:

        try:
            wID = workers[g]

            for q in questionaire_data_raw[1:]:
                
                if q[quest_workerID_index] == wID:
                    englishComp = q[quest_english_comp]

                    if int(englishComp) < 5:
                        print(f"GUID: {g}: WorkerID: {wID} has an English comprehension of: {englishComp}")
        except:
            print(f"GUID: {g} does not have a corresponding worker")


