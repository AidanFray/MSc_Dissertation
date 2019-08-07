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


workers = {
    # Round 2
    "bc86a512-dbc4-423b-8bf5-cfb4b9b9a0f5" : "A3AY0315YWWNXY",
    "2def8ef3-d256-49ef-b7fd-dfb37dc5503a" : "A1E8PIR82KIJEP",

    # Round 3
    "1d22f1c4-343c-414e-a88e-e18d1e1018d4" : "A2K5S80NT1PKK4",
    "4b4cec4c-1135-4865-8f8b-ed757672d1ee" : "A186MBH9JN8ED9",

    # Round 4
    "465499ac-b1df-429c-adde-7bfb7934df54" : "APY5858P6BTDY",
    "f77211f3-e3a0-48a5-b8a1-1fb82bdb2ca8" : "AJTLLYV8O5FQU",
    "c4f0dd4b-8e83-41d7-bd22-3f9fee8d2b4c" : "A371H3PQPR2Z8J",
    "0d7ad13b-dc78-4221-87b5-09c04f70a76d" : "A2N825X4R5H7EK",
    "a7bb25d9-e396-430a-a6d3-245b0a71a79e" : "AYUZGGAGNM9FT",
    "60b6c3f3-f009-432e-89d3-811aa4b87261" : "A1F1BIPJR11LSR",
    "09253673-edd7-41ff-8d6e-18647d439f7b" : "A32W24TWSWXW",
    "f16d526d-0568-4a83-b70a-efdf92a40791" : "A2XRTITADBPWK6",
    "f1368329-c7a5-4511-9326-decdbe16a10b" : "A192MH226Q1NT4",
    "2b669056-64e6-4b73-bf70-73e0b4a8086a" : "A2J84AUK1GVTEA",
}

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
            print(f"GUID: {g} does not have a corresponding worker. ", end="")
            print("Moving to a separate directory...")
            os.system(f"mv {target_dir}{g}.pkl {target_dir}/NoWorker")
