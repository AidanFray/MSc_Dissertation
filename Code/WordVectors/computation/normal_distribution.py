import matplotlib
matplotlib.use('GTK3Agg') 

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
    with open(fileName + "/values.dat") as file:
        data = file.read()

    data = data.strip()

    # For legacy data that was split with a ", "
    data = data.replace(" ", "")
    
    values = data.split(",")
    values = list(map(str.strip, values))
    
    for index, value in enumerate(values):

        float_val = None
        try:
            float_val = float(value)

            values[index] = float_val
        except ValueError:

            # Deletes erroneous value
            del values[index]

    return values

def plot_distribution(data):
    sns.distplot(data, hist = False, kde = True, kde_kws = {'linewidth': 2, 'shade': True})

def pickle_plot():
    ax = plt.subplot()
    pickle.dump(ax, open(f"mplfigure_{int(time.time())}.pkl", "wb"))

if __name__ == "__main__":
    # fileNames = ["pgp_odd_data", "pgp_even_data", "peerio"]
    fileNames = ["dictionary_popular"]


    print("[*] Loading data.....", end="")
    sys.stdout.flush()
    data = np.get  (fileNames[0] + "/memmap.dat", dtype="float32", mode="r", shape=(1, ))
    print("[OK]")

    x = data[0:100]
    print(x)

    plot_distribution(x)
    pickle_plot()