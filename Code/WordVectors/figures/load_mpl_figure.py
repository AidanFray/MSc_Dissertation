#! /usr/bin/python3 
import sys
import pickle as pl
import matplotlib.pyplot as plt
import numpy as np

# TODO: Find out how to change the colour of the shade for the distributions

"""
Scripts to load and view a Matplotlib graph
"""

def usage():
    print("Usage: ./load_mpl_figure.py <FIGURE_PATH>")
    exit()

if len(sys.argv) < 2:
    usage()
    
paths = sys.argv[1:]

# # DEBUG
# paths = ["./Code/WordVectors/figures/solo/peerio/figure.pkl"]

for p in paths:
    ax = pl.load(open(p, "rb"))

line_names = ax.legend_.texts
print("[*] Would you like to set colours? (y/N)")
ans = input(">>> ")

if ans == "Y":
    for index, value in enumerate(ax.lines):
        code = input(f"[*] Enter the colour code for \"{line_names[index]._text}\" ")

        if code != "":
            value.set_color(code)
    
# plt.grid(True)
plt.show()
