#!/usr/bin/env python

import sys
import glob
import re

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText

from xvg2png import xvg2array, xvg2array_eb
import q_acc

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

    if options.legend:
        at = AnchoredText(options.legend,
                          prop=dict(size=24), frameon=True,
                          loc=1,)

    # template must be specified
    elif options.template_for_legend:
        at = AnchoredText(
            re.compile(options.template_for_legend).search(inf).group(),
            prop=dict(size=24), frameon=True, loc=1,)
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        ax.add_artist(at)
    else:
        ax.legend()

    if options.title:
        ax.set_title(title)
    return id_, x, y

def main(options):
    infs = options.fs
    len_infs = len(infs)

    if options.overlap:
        overlap = options.overlap
        assert len_infs % overlap== 0, "the num of infiles are not even to do overlap"
        row, col = q_acc.det_row_col(len_infs / overlap, options.morer)
    else:
        overlap = 1
        row, col = q_acc.det_row_col(l, options.morer)

    fig = plt.figure(figsize=(24, 11))
    xs, ys, id_s, axes = {}, {}, [], []
    for k, inf in enumerate(infs):
        if k % overlap == 0:
            ax = fig.add_subplot(row, col, k / overlap + 1)

        id_, x, y = ax_plot(inf, ax, options)
        axes.append(ax)
        id_s.append(id_)
        xs[id_], ys[id_] = x, y
    q_acc.decorate(id_s, xs, ys, axes, options)
    q_acc.show_or_save(options.of)

if __name__ == '__main__':
    import time; b=time.time()
    options = q_acc.parse_cmd()
    main(options)
    e = time.time()
    print e - b
