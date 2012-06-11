#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import matplotlib.path as path

from xvg2png import xvg2array_data_points
import q_acc

"""
The major difference between q_pdf2.py and q_pdf.py is that the former one uses
np.histogram instead of ax.hist.

adjusted for long line with numerous data points, plotting distributions

"""

def ax_distri(inf, ax, bins):
    id_ = inf
    y = xvg2array_data_points(inf)
    len_y = float(len(y))
    print len_y, inf

    # bins must be assigned in options
    n, b = np.histogram(y, bins, normed=False)

    b = (b[:-1] + b[1:]) / 2.                               # to gain the same length as n
    n = n / len_y                                           # normalized by len_y

    import sys
    for bi, ni in zip(b, n):
        sys.stdout.write('{0:8.5f} {1:18.8f}\n'.format(bi, ni))

    # p = ax.plot(b, n, linewidth=2, label=inf)
    ax.plot(b, n, linewidth=2, label=inf)
    return id_, n, b

def outline():
    infs = options.fs
    print infs
    lenf = len(infs)

    if options.overlap:
        olp = options.overlap
        assert lenf % olp== 0, (
            "the num of infiles (%d) cannot be divided exactly by overlap (%d)" % (lenf, olp))
        row, col = q_acc.det_row_col(lenf/olp, options.morer)
    else:
        olp = 1
        row, col = q_acc.det_row_col(lenf, options.morer)

    fig = plt.figure(figsize=(24, 11.6625))
    ns, bs, id_s, axes = {}, {}, [], []
    for k, inf in enumerate(infs):
        if k % olp == 0:
            ax = fig.add_subplot(row, col, k/olp+1)
        id_, n, b = ax_distri(inf, ax, options.bins)
        axes.append(ax)
        id_s.append(id_)
        ns[id_], bs[id_] = n, b
    q_acc.decorate(
        id_s, bs, ns, axes, options.blegend, 
        options.xlb, options.ylb,
        options.xb, options.xe,
        options.yb, options.ye,
        )
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
