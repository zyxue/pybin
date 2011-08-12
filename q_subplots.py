#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import sys
import glob
from xvg2png import xvg2array, xvg2array_eb
import q_acc
# from Mysys import read_mysys_dat

# MYSYS = read_mysys_dat()

def ax_plot(inf, ax, options):
    id_ = inf
    if options.eb:
        x, y, e = xvg2array_eb(inf, options.xcol, options.ycol)
        x = x/1000. if options.nm else x
        ax.errorbar(x,y,yerr=e, label=id_)
    else:
        x, y = xvg2array(inf)
        x = x/1000. if options.nm else x
        p = ax.plot(x,y, label = inf) 
    ax.legend()
    # ax.set_title(inf)
    return id_, x, y

def outline(options):
    infs = sorted(glob.glob(options.fs))
    l = len(infs)

    if options.overlap:
        olp = options.overlap
        assert l % olp== 0, "the num of infiles are not even to do overlap"
        row,col = q_acc.det_row_col(l/olp, options.morer)
    else:
        olp = 1
        row,col = q_acc.det_row_col(l,options.morer)

    fig = plt.figure(figsize=(24,11))
    xs, ys, id_s, axes = {}, {}, [], []
    for k, inf in enumerate(infs):
        if k % olp == 0:
            ax = fig.add_subplot(row,col,k/olp+1)

        id_, x, y = ax_plot(inf, ax, options)
        axes.append(ax)
        id_s.append(id_)
        xs[id_], ys[id_] = x, y
    q_acc.decorate(id_s, xs, ys, axes, options)
    q_acc.show_or_save(options.of)

if __name__ == '__main__':
    import time; b=time.time()
    options = q_acc.parse_cmd()
    outline(options)
    e = time.time()
    print e - b
