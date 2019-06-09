import sys
import pickle as pl
import matplotlib.pyplot as plt
import numpy as np

"""
Scripts to load and view a Matplotlib graph
"""

def usage():
    print("Usage: ./load_mpl_figure.py <FIGURE_PATH>")
    exit()

if len(sys.argv) < 2:
    usage()

paths = sys.argv[1:]

for p in paths:
    
    a = pl.load(open(p, "rb"))

plt.show()

