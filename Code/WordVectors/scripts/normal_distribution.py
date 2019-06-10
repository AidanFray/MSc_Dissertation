import matplotlib
# matplotlib.use('Agg') 
matplotlib.interactive(False)

import matplotlib.pyplot as plt

import seaborn as sns
import scipy.stats as stats
import numpy as np
import pickle
import math
import time
import sys

"""
Scripts that plots the normal distribution of a set of files from numpy arrays
"""

def load_data(fileName):
    
    data = []
    with open(fileName) as file:
        for line in file:
            data.append(float(line.strip()))

    return data

def plot_distribution(data):
    sns.distplot(data, bins=500, hist = True, kde = True, kde_kws = \
        {
            'linewidth': 1,
            # 'linestyle': "--",
            'shade': True
        }
    )

def pickle_plot():
    ax = plt.subplot()
    pickle.dump(ax, open(f"mplfigure_{int(time.time())}.pkl", "wb"))

if __name__ == "__main__":

    fileNames = sys.argv[1:]

    print("[*] Plotting data")
    sys.stdout.flush()
    for f in fileNames:
        print(f"[*] Plotting: {f}")
        plot_distribution(load_data(f))

    plt.legend(fileNames)
    pickle_plot()

    plt.show()