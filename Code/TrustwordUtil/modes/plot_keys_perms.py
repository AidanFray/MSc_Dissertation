import sys
sys.path.append("..")
sys.path.append("./trustword_util/util")

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import statistics

from util.permutations import *
from util.trustwords import *
from util.mappings import *
from util.load import *

NUM_OF_WORDS = 4

def load_keys_and_parse(filePath):

    keys = []
    with open(filePath) as file:

        for line in file:
            keys.append(line[:NUM_OF_WORDS * 4])

    return keys

def plot_distribution(data):
    sns.distplot(data, bins=1000, hist = True, kde = False, kde_kws = \
        {
            'linewidth': 1,
            'linestyle': "--",
            'shade': True
        }
    )

    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.xlabel("Number of permutations")
    plt.ylabel("Number of keys")

    f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
    g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(g))
    plt.show()


def plot(vulnKeyFilePath, staticWordsVal, mapping):
    
    keys = load_keys_and_parse(vulnKeyFilePath)

    static_pos = []
    if staticWordsVal == 2:
        static_pos = [0, 3]
    elif staticWordsVal == 1:
        static_pos = [0]

    total_loops = len(keys)

    all_permutations = []

    for i, k in enumerate(keys):
        trustwords = fingerprint_to_words(k, mapping, PRINT=False)

        num_of_perms = similar_perms_size(trustwords, mapping, staticPos=static_pos)

        # num_of_perms == 0 is when RAM protection activates
        if num_of_perms != 0:
            all_permutations.append(num_of_perms)
    
    # plot_distribution(all_permutations)
    print("Average: ", sum(all_permutations)/len(all_permutations))
    print("StDev: ", statistics.stdev(all_permutations))

