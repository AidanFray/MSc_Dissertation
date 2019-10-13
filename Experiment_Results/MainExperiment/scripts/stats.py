import httpagentparser
import experiment
import matplotlib.pyplot as plt
import statistics
import operator
import pickle
import csv
import sys
import os

AGE_RANGES = {
    range(18, 25): 0,
    range(25, 30): 0,
    range(30, 40): 0,
    range(40, 50): 0,
    range(50, 60): 0,
    range(60, 70): 0,
    range(70, 80): 0
}

def usage():
    print(f"Usage: python {__name__} <TARGET_DIR> <HIT_DATA> <DEMOGRAPHIC_DATA>")
    exit()

def load_csv(filePath):
    data = []
    with open(filePath) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row)

    return data

def average(lst):
    return round(sum(lst)/len(lst), 2)

def parse_hit_file(hitData):

    workerId_index = hitData[0].index("WorkerId")
    guid_index = hitData[0].index("Answer.surveycode")

    # Alterations
    workers = {
        "A3AY0315YWWNXY" : "bc86a512-dbc4-423b-8bf5-cfb4b9b9a0f5",
        "A1E8PIR82KIJEP" : "2def8ef3-d256-49ef-b7fd-dfb37dc5503a",
        "A2K5S80NT1PKK4" : "1d22f1c4-343c-414e-a88e-e18d1e1018d4",
        "A186MBH9JN8ED9" : "4b4cec4c-1135-4865-8f8b-ed757672d1ee",
        "APY5858P6BTDY"  : "465499ac-b1df-429c-adde-7bfb7934df54",
        "AJTLLYV8O5FQU"  : "f77211f3-e3a0-48a5-b8a1-1fb82bdb2ca8",
        "A371H3PQPR2Z8J" : "c4f0dd4b-8e83-41d7-bd22-3f9fee8d2b4c",
        "A2N825X4R5H7EK" : "0d7ad13b-dc78-4221-87b5-09c04f70a76d",
        "AYUZGGAGNM9FT"  : "a7bb25d9-e396-430a-a6d3-245b0a71a79e",
        "A1F1BIPJR11LSR" : "60b6c3f3-f009-432e-89d3-811aa4b87261",
        "A32W24TWSWXW"   : "09253673-edd7-41ff-8d6e-18647d439f7b",
        "A2XRTITADBPWK6" : "f16d526d-0568-4a83-b70a-efdf92a40791",
        "A192MH226Q1NT4" : "f1368329-c7a5-4511-9326-decdbe16a10b",
        "A2J84AUK1GVTEA" : "2b669056-64e6-4b73-bf70-73e0b4a8086a",
    }

    for h in hitData[1:]:

        if not h[workerId_index] in workers:
            workers.update({h[workerId_index] : h[guid_index]})

    return workers

def parse_demographic_data(demoData, workerToGuid):
    
    workerId_index = demoData[0].index("Worker ID")
    timestamp_index = demoData[0].index("Timestamp")

    worker_data = {}
    for d in demoData[1:]:
        
        ID = d[workerId_index].strip()

        del d[workerId_index]
        del d[timestamp_index]

        try:
            worker_data.update({workerToGuid[ID]: d})
        except KeyError:
            # Ignores phatom users
            pass

    return worker_data

def user_agent_parsing(experiments):

    print("[!] UserAgent Parsing\n")

    # operatingSystems = {}
    # for e in experiments:
    #     user_agent = httpagentparser.detect(e.UserAgent)

    #     platformName = user_agent['platform']['name'].strip()
    #     version = user_agent['platform']['version']

    #     if not platformName in operatingSystems:
    #         operatingSystems.update({platformName: [version]})
    #     else:
    #         operatingSystems[platformName].append(version)

    # for os in operatingSystems:
    #     print("\t", os, len(operatingSystems[os]))
    # print("\n\t Total:", len(experiments))

    operating_systems = {}
    browsers = {}
    for e in experiments:
        user_agent = httpagentparser.simple_detect(e.UserAgent)

        platform = user_agent[0]

        browser = user_agent[1].split(" ")[0]

        if not platform in operating_systems:
            operating_systems.update({platform: 1})
        else:
            operating_systems[platform] += 1

        if not browser in browsers:
            browsers.update({browser: 1})
        else:
            browsers[browser] += 1

    print("\t [*] Operating systems")
    for os in operating_systems:
        print(f"\t   {os}: {operating_systems[os]} -- {round(operating_systems[os] / len(experiments) * 100, 2)}%")

    print()
    print("\t [*] Browswers: ")
    for b in browsers:
        print(f"\t   {b}: {browsers[b]}")

def average_completion_time(experiments):
    
    print("\n[!] Average completion time:")
    all_times = []
    non_attack_times = []
    attack_times = []

    for e in experiments:

        if len(e.RoundStartTimes) == len(e.RoundEndTimes):

            totalTime = e.EndTime - e.StartTime
            if totalTime > 2000:
                #print(f"\t {e.ExperimentID} has a long total time: {totalTime}")
                pass
            else:
                times = list(map(operator.sub, e.RoundEndTimes, e.RoundStartTimes))

                for i, t in enumerate(times):

                    # Not an attack
                    if e.AttackSchema[i] == None:
                        non_attack_times.append(t)

                    # An attack
                    else:
                        attack_times.append(t)

                all_times += times
                plt.plot(times)

    # plt.ylim(0, 100)
    # plt.show()
    print()
    print(f"\tAverage: \t\t{average(all_times)} seconds ")
    print(f"\tAttack average: \t{average(attack_times)} seconds ")
    print(f"\tNon-attack average: \t{average(non_attack_times)} seconds ")
    
def false_positive_rate(experiments):
    print("\n[!] False positives: ")

    non_attacks = 0
    false_positives = 0

    for e in experiments:
        
        for i, a in enumerate(e.AttackSchema):
            
            if a == None:
                non_attacks += 1
            
            if e.Responses[i] == "False" and a == None:
                false_positives += 1

    print(f"\n\tOccurrence in non-attack rounds: \n\t  {round((false_positives/non_attacks) * 100, 2)}%")

def attack_breakdown(experiments):
    print("\n[!] Attack stats: \n")
    
    all_attacks = 0
    successful_attacks = 0

    # List: [Successful: Total]
    attack_metrics = {
        "LEVEN":        [0, 0], 
        "METAPHONE":    [0, 0], 
        "NYSIIS":       [0, 0]
    }

    # List: [<0 static>, <1 static>, <2 static>]
    #   
    #    <X static> = [Successfull, Total]
    attack_types = {
        "LEVEN":     [[0, 0], [0, 0], [0, 0]],
        "METAPHONE": [[0, 0], [0, 0], [0, 0]],
        "NYSIIS":    [[0, 0], [0, 0], [0, 0]]
    }

    for e in experiments:

        for i, a in enumerate(e.AttackSchema):

            if a != None:
                all_attacks += 1

                # Increments the total occurrence of the metric
                attack_metrics[a[0]][1] += 1

                # Yucky - increments the total amount
                attack_types[a[0]][a[1]][1] += 1

                if e.Responses[i] == "True":

                    # Increments the successfull attacks
                    attack_metrics[a[0]][0] +=1

                    # Increments the attack type successfull attacks
                    attack_types[a[0]][a[1]][0] += 1

                    successful_attacks += 1

    print(f"\t Overall attack success rate: \t{round((successful_attacks/all_attacks) * 100, 2)}%")
    print(f"\t Number of total attacks: \t{all_attacks}")
    print(f"\t Total rounds: \t\t\t{len(experiments) * 30}")

    print()
    for a in attack_metrics:
        overall_average = round(attack_metrics[a][0] / attack_metrics[a][1] * 100, 2)

        print(f"\t {a} - \t{attack_metrics[a]} - {overall_average}%")

        for i, t in enumerate(attack_types[a]):

            average_success = round(t[0] / t[1] * 100, 2)

            print(f"\t\t\t  {i} static - {t} - {average_success}%")
        print()

def demographical_stats(workerData, experiments):

    print("\n[!] Demographical Data: ")

    GENDER_TALLY = {
        "Male": 0, 
        "Female": 0
    }

    EDUCATION_TALLY = {
        "GCSE": 0,
        "A-Level / O-Level": 0,
        "Bachelor's degree": 0,
        "Master's degree": 0, 
        "PhD": 0
    }

    AGES = []

    for e in experiments:

        ID = e.ExperimentID

        try:

            data = workerData[ID]

            gender = data[0]
            age = int(data[1])
            education = data[2]

            # Gender
            GENDER_TALLY[gender] += 1

            # Education
            EDUCATION_TALLY[education] += 1

            # Tallies the ages
            for a in AGE_RANGES:
                if age in a:
                    AGE_RANGES[a] += 1
                    break

            AGES.append(age)

        except KeyError:
            print(f"\t Worker did not fill out the questionaire for {ID}")

    print("\n\t [*] Gender: \n")
    for g in GENDER_TALLY:
        print(f"\t  {g} - {round(GENDER_TALLY[g] / len(experiments) * 100, 2)}%")

    print("\n\t [*] Ages: \n")
    for a in AGE_RANGES:
        print("\t  ", f"{a[0]}-{a[-1]} - {round(AGE_RANGES[a] / len(experiments) * 100, 2)}%")

    print(f"\t  Average: {round(sum(AGES)/len(AGES), 2)}")
    print(f"\t  Standard Deviation : {round(statistics.stdev(AGES), 2)}")

    print("\n\t [*] Highest Education: \n")
    for e in EDUCATION_TALLY:
        print(f"\t  {e}: \n\t   {round(EDUCATION_TALLY[e] / len(experiments) * 100, 2)}%\n")

def education_and_attack_link(workerData, experiments):

    print("[!] Education and number of attacks: ")

    educationAndAttack = {}

    for e in experiments:

        ID = e.ExperimentID

        try:
            data = workerData[ID]
            education = data[2]


            totalAttack = 0
            successfullAttack = 0
            for i, a in enumerate(e.AttackSchema):

                if a != None:
                    totalAttack += 1

                    if e.Responses[i] == "True":
                        successfullAttack += 1

            if not education in educationAndAttack:
                educationAndAttack.update({education: [successfullAttack, totalAttack]})
            else:
                educationAndAttack[education][0] += successfullAttack
                educationAndAttack[education][1] += totalAttack
        except KeyError:
            pass


    for ea in educationAndAttack:
        percentage = round(educationAndAttack[ea][0] / educationAndAttack[ea][1] * 100, 2)
        print("\t   ", ea, educationAndAttack[ea], f"{percentage}%")


if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        usage()

    target_dir = sys.argv[1]
    hit_path = sys.argv[2]
    demographic_path = sys.argv[3]

    # Loads in externel files
    workerToGuid = parse_hit_file(load_csv(hit_path))
    workerData = parse_demographic_data(load_csv(demographic_path), workerToGuid)

    experiments = []
    for file in os.listdir(f"{target_dir}"):

        if file.endswith(".pkl"):
            
            f = target_dir + file
            exp = pickle.load(open(f, "rb"))

            experiments.append(exp)

    print(f"[!] Number of participants: {len(experiments)}")

    attack_breakdown(experiments)
    average_completion_time(experiments)
    false_positive_rate(experiments)
    demographical_stats(workerData, experiments)
    user_agent_parsing(experiments)
    
    education_and_attack_link(workerData, experiments)

