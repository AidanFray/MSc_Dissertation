import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import numpy as np
import math
import sys

"""
Scripts that plots the normal distribution of a set of files from numpy arrays
"""

def load_data(fileName):
    
    data = []
    with open(fileName + "/values.dat") as file:
        data = file.read()

    data = data.strip()

    # For legacy data that was split with a ", "
    data = data.replace(" ", "")
    
    values = data.split(",")
    values = list(map(str.strip, values))
    values = list(map(float, values))

    return values

def plot_distribution(data):
    sns.distplot(data, hist = False, kde = True, kde_kws = {'linewidth': 2, 'shade': True})


if __name__ == "__main__":
    fileNames = ["pgp_odd_data", "pgp_even_data", "peerio"]

    print("[*] Loading data....", end="")
    sys.stdout.flush()
    data_points = []
    for f in fileNames:
        data_points.append(load_data(f))
    print("[OK]")

    for d in data_points:
        plot_distribution(d)

    plt.legend(fileNames)
    plt.xlabel("Phonetic Distance")
    plt.ylabel("Proportion of words")
    plt.show()
