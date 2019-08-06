from MTurk import *
import sys

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        usage()

    mainWorkerData = load(sys.argv[1])
    hitWorkerData = load(sys.argv[2])

    qualiHeaderPosition = mainWorkerData[0].index('UPDATE-Trustwords')

    workerIdPosition = hitWorkerData[0].index('WorkerId')

    for hit in hitWorkerData[1:]:
        workerID = hit[workerIdPosition]

        for i, m in enumerate(mainWorkerData[1:]):
            if m[0] == workerID:

                mainWorkerData[i + 1][qualiHeaderPosition] = '1'
                break

        else:
            # raise Exception("Error: Worker ID not found!")
            print(f"[!] Worker: {workerID} not found!")
            pass
            
    save("User.csv", mainWorkerData)
