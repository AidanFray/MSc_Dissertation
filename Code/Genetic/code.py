import random
from deap import creator, base, tools, algorithms


SUBSET_SIZE = 1024
POPULATION_SIZE = 10

# TODO: Generate a random population of subsets of words
def create_population(words):
    pass

# TODO: Breed them by swapping members
def breed(m1, m2):
    pass

# TODO: Define a function to determine the overall fitness of the subset
#           - The fitness function could be the sum of all the distances? 
#             I would, therefore, want to create the largest value
def fitness(m):
    pass

def load_wordlist(filePath):
    """
    Loads the wordlist into a list
    """

    with open(filePath) as file:
        data = file.readlines()

    return data

WORDLIST = "/home/user/Github/Cyber-Security-Individual-Project/Wordlists/Trustwords/EN/en_unique.csv"

if __name__ == "__main__":
    words = load_wordlist(WORDLIST)
