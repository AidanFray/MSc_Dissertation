import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import numpy as np
import math


def load_data(fileName):
    
    data = []
    with open(fileName) as file:
        data = file.read()

    data = data.strip()

    values = data.split(", ")
    values = list(map(str.strip, values))
    values = list(map(float, values))

    return values

def plot_distribution(data):
    sns.distplot(data, hist = False, kde = True, kde_kws = {'linewidth': 2, 'shade': True})


if __name__ == "__main__":
    # fileNames = ["pgp_odd_data/values.dat", "pgp_even_data/values.dat", "peerio/values.dat"]
    fileNames = ["pgp_odd_data/values.dat", "pgp_even_data/values.dat"]

    data_points = []
    for f in fileNames:
        data_points.append(load_data(f))


    print(len(data_points))
    for d in data_points:
        plot_distribution(d)

    plt.legend(fileNames)
    plt.xlabel("Phonetic Distance")
    plt.ylabel("Proportion of words")
    plt.show()