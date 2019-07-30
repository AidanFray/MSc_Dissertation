import sys

def usage():
    print("Usage ./{__file__} <RESULTS_CSV>")
    exit()

def parse(filepath):
    responses = []
    with open(filepath) as file:
        responses = file.readlines()

    # Removes the headers
    del responses[0]

    for r in responses:

        parts = r.split(",")
        
        sectionsParts = parts[4:len(parts) - 6]
        testQuestions = parts[len(parts) - 5:len(parts) - 2]


        sections = []
        for i, s in enumerate(sectionsParts[::5]):
            index = i * 5
            sections += [sectionsParts[index:index + 5]]

        randomSection = list(map(int, sections[-1]))
        print(f"[*] Random average: {sum(randomSection) / len(randomSection)}", )




if __name__ == "__main__":

    if len(sys.argv)!= 2:
        usage()

    parse(sys.argv[1])
