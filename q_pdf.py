#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import glob
from xvg2png import xvg2array
import q_acc

def ax_distri(inf, ax, bins):
    y = xvg2array(inf)[1]
    id_ = inf
    n, b, patches = ax.hist(y, bins, normed=True, label=inf, histtype='step')
    ax.legend()
    return id_, n, b, patches

def outline():
    infs = sorted(glob.glob(options.fs))
    l = len(infs)

    if options.overlap:
        olp = options.overlap
        assert l % olp== 0, (
            "the num of infiles (%d) cannot be divided exactly by overlap (%d)" % (l, olp))
        row, col = q_acc.det_row_col(l/olp, options.morer)
    else:
        olp = 1
        row, col = q_acc.det_row_col(l, options.morer)

    fig = plt.figure(figsize=(24, 11.6625))
    ns, bs, id_s, axes = {}, {}, [], []
    for k, inf in enumerate(infs):
        if k % olp == 0:
            ax = fig.add_subplot(row, col, k/olp+1)
        id_, n, b ,patches = ax_distri(inf, ax, options.bins)
        axes.append(ax)
        id_s.append(id_)
        ns[id_], bs[id_] = n, b
    q_acc.decorate(id_s, bs, ns, axes, options)
    q_acc.show_or_save(options.of)

if __name__ == '__main__':
    # import cProfile
    # cProfile.run('outline(options)')
    import time; b = time.time()
    global options
    options = q_acc.parse_cmd()
    outline()
    e = time.time()
    print e - b

