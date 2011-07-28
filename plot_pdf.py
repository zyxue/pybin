#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.patches as patches
import matplotlib.path as path
import glob
from xvg2png import xvg2array_nt
from det_row_col import det_row_col
from Mysys import read_mysys_dat
from q_cluster import det_lim, decorate, parse_cmd, show_or_save

mysys = read_mysys_dat()

"""Probability Densitry Function"""


def ax_distri(inf,ax,bins):
    print inf
    y = xvg2array_nt(inf) # when plotting distribution, time dependence is not
                          # important, xvg2array_nt will increase speed a lot
    bi = inf.find('sq'); id = inf[bi:bi+4]
    n,b,patches = ax.hist(y,bins,normed=True,color=mysys[id].col,label=mysys[id].seq,histtype='step')
    return id, n, b, patches

def outline(options):
    infs = sorted(glob.glob(options.fs))
    fig = plt.figure(figsize=(24,11.6625))
    if options.mw:
        assert len(infs)%2 == 0, "the num of infiles are not even to do mw overlap"
        row, col = det_row_col(len(infs)/2)
    else:
        row,col = det_row_col(len(infs))
    ns = {}                     # collection of n, containing the number of bins
    bs = {}                     # collection of bins
    ids = []
    axes = []
    for k, inf in enumerate(infs):
        if options.mw:                            # options.mw action=store_true
            if k%2 == 0:                          # overlap for m300 & w300
                ax = fig.add_subplot(row,col,k/2+1); axes.append(ax)
        else:
            ax = fig.add_subplot(row,col,k+1); axes.append(ax)
        id, n, b ,patches = ax_distri(inf,ax,options.bins)
        ids.append(id)
        ns[id] = n
        bs[id] = b
    decorate(ids,bs,ns,axes,options)
    show_or_save(options.of)

if __name__ == '__main__':
    # import cProfile
    # cProfile.run('outline(options)')
    import time; b = time.time()
    outline(parse_cmd())
    e = time.time()
    print e - b

