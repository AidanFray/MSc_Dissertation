import sys
import pickle as pl
import matplotlib.pyplot as plt
import numpy as np

"""
Scripts to load a view a Matplotlib graph
"""

def usage():
    print("Usage: ./load_mpl_figure.py <FIGURE_PATH>")
    exit()

if len(sys.argv) != 2:
    usage()

path = sys.argv[1]

ax = pl.load(open(path, "rb"))
plt.show()

