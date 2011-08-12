#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import glob
# from mpl_toolkits.axes_grid1.parasite_axes import SubplotHost
from xvg2png import xvg2array
import q_acc
from Mysys import read_mysys_dat

mysys = read_mysys_dat()

VERSION = '3.0'

def ax_ave(xyf, ax):
    xf, yf = xyf
    xp, yp = xvg2array(xf)[1], xvg2array(yf)[1]
    (ave_xp, std_xp, ave_yp, std_yp) = (
        np.average(xp), np.std(xp), np.average(yp), np.std(yp))
    tid = q_acc.get_id(xyf)
    sid = tid[:3]
    cid = tid[3]
    ax.errorbar(ave_xp, ave_yp, xerr=std_xp, yerr=std_yp,
                c=mysys[cid].col, marker=mysys[sid].char,
                label=mysys[sid].seq+sid, markersize=10)
    # ax.text(p1[0]*1.01,p2[0]*1.01,p1_file[5:12])
    return tid, ave_xp, std_xp, ave_yp, std_yp

def outline(options):
    xfs = sorted(glob.glob(options.xf))
    yfs = sorted(glob.glob(options.yf))
    if len(xfs) != len(yfs):
        raise ValueError(
            "the number of xyfs are not the same!!\n%r\n%r" % (xfs, yfs))

    fig = plt.figure(figsize=(12,9))
    ax = fig.add_subplot(1,1,1)
    xps, yps, tids, axes = {}, {}, [], [ax]
    for k, xyf in enumerate(zip(xfs,yfs)):
        print xyf
        tid, ave_xp, std_xp, ave_yp, std_yp = ax_ave(xyf,ax)
        tids.append(tid)
        xps[tid] = [ave_xp-std_xp, ave_xp+std_xp]
        yps[tid] = [ave_yp-std_yp, ave_yp+std_yp]
    ax.legend()
    q_acc.decorate(tids,xps,yps,axes,options)
    q_acc.show_or_save(options.of)
    
if __name__ == '__main__':
    import time; b = time.time()
    options = q_acc.parse_cmd()
    outline(options)
    e = time.time()
    print e - b

