#!/usr/bin/env python

import sys
import glob
import re

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText

from xvg2png import xvg2array, xvg2array_eb
import q_acc

def ax_plot(inf, ax, legend, color, marker, berrorbar=False):
    """keys in kwargs could be: legend, title, color, marker"""
    label = legend
    if berrorbar:
        x, y, e = xvg2array_eb(inf, options.xcol, options.ycol)
        x = x/1000. if options.nm else x
        ax.errorbar(x, y, yerr=e, label=label)
    else:
        x, y = xvg2array(inf)
        x = x/1000. if options.nm else x
        if color and marker:
            p = ax.plot(x, y, color=color, marker=marker, label=label) 
        elif color:
            p = ax.plot(x, y, color=color, label=label) 
        elif marker:
            p = ax.plot(x, y, marker=marker, label=label) 
        else:
            p = ax.plot(x, y, linewidth=2, label=label) 
    return x, y

def main(options):
    infs = options.fs
    len_infs = len(infs)

    if options.mysys:
        from Mysys import read_mysys_dat
        mysys = read_mysys_dat()
    else:
        mysys = None

    if options.overlap:
        overlap = options.overlap
        assert len_infs % overlap== 0, "the num of infiles are not even to do overlap"
        row, col = q_acc.det_row_col(len_infs / overlap, options.morer)
    else:
        overlap = 1
        row, col = q_acc.det_row_col(len_infs, options.morer)
    
    fig = plt.figure(figsize=(24, 11))
    xs, ys, keys, axes = {}, {}, [], []
    for k, inf in enumerate(infs):
        if k % overlap == 0:
            ax = fig.add_subplot(row, col, k / overlap + 1)

        if options.template_for_legend:
            legend = re.compile(options.template_for_legend).search(inf).group()
        else:
            legend = inf

        if mysys:
            # need further modification to choose color in terms of solute or solvent
            group = re.compile('sq[1-9][wmepov]\d{3,4}s[0-9][0-9]').search(inf).group()
            seq = group[:3]
            color = mysys[seq].color
            marker = mysys[seq].marker
            legend = mysys[seq].seq
        else:
            color = None                # specified by matplotlib automatically
            marker = None

        key = inf                                  # use the file name as a key
        # collection of x & y will be used to determine the xlim & ylim
        x, y = ax_plot(inf, ax, legend, color, marker, options.eb)
        axes.append(ax)
        keys.append(key)
        xs[key], ys[key] = x, y

    blegend, xlb, ylb, xb, yb, xe, ye = (options.blegend, options.xlb, options.ylb, 
                                         options.xb, options.yb, options.xe, options.ye)
    q_acc.decorate(keys, xs, ys, axes, blegend, xlb, ylb, xb, yb, xe, ye)
    q_acc.show_or_save(options.of)

if __name__ == '__main__':
    import time; b=time.time()
    options = q_acc.parse_cmd()
    main(options)
    e = time.time()
    print e - b
