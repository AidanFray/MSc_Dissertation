import sys

"""
Parses the results from the Google Forms pilot study
"""

NUM_OF_DEMOGRAPHIC_QUESTIONS = 4

# This is questions added after the first launch of the survery
# Google Sheets does not try to maintain the order so new questions
# are added to the end
#       
#   1. English proficiency
#   2. Attension question "UNIVERSITY-UNIVERSITY"
#   3. Attension question "DYNAMIC-DYNAMIC"
NEWLY_ADDED_QUESTIONS = 6

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

def order_results(filepath):
    responses = []
    with open(filepath) as file:
        responses = file.readlines()

    # Removes the headers
    del responses[0]

    # Splits data into 5x5 sections
    for r in responses:

        parts = r.split(",")

        # HACK: Removes the english ability question added later 
        parts = parts[:-(NEWLY_ADDED_QUESTIONS + 1)]

        # Prints out each section
        response_sections = []
        for x in range(NUM_OF_DEMOGRAPHIC_QUESTIONS, len(parts), 5):

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

        total = 0
        num_of_values = 0
        missed = 0

        for response in sect_results:

            for value in response:

                if value != "":
                    total += int(value)
                    num_of_values += 1
                else:
                    missed += 1

        print(sect)
        print(f"[!] Average : {round(total/num_of_values, 2)}")
        print(f"[!] Missed  : {missed}")
        print()

            
