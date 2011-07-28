#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import sys
import glob
from xvg2png import xvg2array_ap
from det_row_col import det_row_col
from q_cluster import parse_cmd, show_or_save
from Mysys import read_mysys_dat

"""quickly plot all properties in a single xvg file"""

def outline(options):
    data = xvg2array_ap(options.fs)
    x = data.pop('time')       # pop the key of 'time' since it will consistent
                               # in all the subplots
    fig = plt.figure(figsize=(24,11))
    row, col = det_row_col(len(data.keys()))
    for k, key in enumerate(data.keys()):
        ax = fig.add_subplot(row,col,k+1)
        print len(x), len(data[key]), key
        ax.plot(x,data[key])
        ax.set_title(key)
        ax.grid(b=True)
    show_or_save(options.of)

if __name__ == '__main__':
    import time; b=time.time()
    outline(parse_cmd())
    e = time.time()
    print "TIME ELAPSED: %f" % (e - b)
