import sys
import statistics

"""
Parses the results from the Google Forms pilot study
"""

NUM_OF_DEMOGRAPHIC_QUESTIONS = 7

# This is questions added after the first launch of the survery
# Google Sheets does not try to maintain the order so new questions
# are added to the end
#       
#   1. Attension question "UNIVERSITY-UNIVERSITY"
#   2. Attension question "DYNAMIC-DYNAMIC"
#   3. Random Average
NEWLY_ADDED_QUESTIONS = 3

SECTIONS = ["Soundex", "Metaphone", "Leven", "NYSIIS", "WordVec", "Random"]

RESULTS = {
    SECTIONS[0] : [],    
    SECTIONS[1] : [],    
    SECTIONS[2] : [],
    SECTIONS[3] : [],
    SECTIONS[4] : [],
    SECTIONS[5] : []
}

def usage():
    print("Usage ./{__file__} <RESULTS_CSV>")
    exit()

def order_results(filepath):
    responses = []
    with open(filepath) as file:
        responses = file.readlines()

    # Removes the headers
    del responses[0]

    # Splits data into 5x5 sections
    for i, r in enumerate(responses):

        parts = r.split(",")

        parts = parts[NUM_OF_DEMOGRAPHIC_QUESTIONS:-(NEWLY_ADDED_QUESTIONS)]

        # Prints out each section
        response_sections = []
        for x in range(0, len(parts), 5):

            section = parts[x:x + 5]
            section = list(map(str.strip, section))

            response_sections.append(section)

        # Adds to the over all results
        for index, resp_sec in enumerate(response_sections):
            RESULTS[SECTIONS[index]].append(resp_sec)

if __name__ == "__main__":
    
    if len(sys.argv)!= 2:
        usage()

    results_filepath = sys.argv[1]
    order_results(results_filepath)
    
    for sect in SECTIONS:

        sect_results = RESULTS[sect]

        all_results = []
        for s in sect_results:
            all_results += s

        all_results = list(filter("".__ne__, all_results))
        all_results = list(map(int, all_results))

        total = 0
        num_of_values = 0
        missed = 0

        for value in all_results:

                if value != "":
                    total += int(value)
                    num_of_values += 1
                else:
                    missed += 1

        print(sect)
        print(f"[!] Average : {round(sum(all_results)/len(all_results), 2)}")
        print(f"[!] Standard Dev: {round(statistics.stdev(all_results), 2)}")
        print(f"[!] Missed  : {missed}")
        print()

            
