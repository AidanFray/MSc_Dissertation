import sys

from MTurk import *

"""
Script that edits MTurk .csv files depending on the result from the study
"""

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        usage()

    mainWorkerFilePath = sys.argv[1]
    hitWorkerFilePath = sys.argv[2]

    mainWorkerData = load(mainWorkerFilePath)
    hitWorkerData = load(hitWorkerFilePath)

    qualiHeaderPosition = mainWorkerData[0].index("\"UPDATE-English Fluency\"")

    answerPosition = hitWorkerData[0].index('\"Answer.howMuch\"') + 1
    workerIdPosition = hitWorkerData[0].index('\"WorkerId\"') + 1
    approveHeaderPosition = hitWorkerData[0].index("\"Approve\"") + 1

    for hit in hitWorkerData[1:]:
        workerID = hit[workerIdPosition]

        mainFileWorkerIDIndex = None
        for i, m in enumerate(mainWorkerData[1:]):
            if m[0] == workerID:
                mainFileWorkerIDIndex = i + 1

                if hit[answerPosition] == '\"5\"':
                    mainWorkerData[mainFileWorkerIDIndex][qualiHeaderPosition] = '1'
                    hit[approveHeaderPosition] = "x"
                break

        else:
            # raise Exception("Error: Worker ID not found!")
            print(f"[!] Worker: {workerID} not found!")
            pass

    save("User.csv", mainWorkerData)
    save("Batch.csv", hitWorkerData)
            