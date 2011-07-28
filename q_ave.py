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
    ave_xp, std_xp, ave_yp, std_yp = np.average(xp), np.std(xp), np.average(yp), np.std(yp)
    pid,sid = q_acc.get_id(xyf)
    id = pid+sid
    ax.errorbar(ave_xp, ave_yp, xerr=std_xp, yerr=std_yp,
                c=mysys[sid].col, marker=mysys[pid].char,
                label=mysys[pid].seq+sid, markersize=10)
    # ax.text(p1[0]*1.01,p2[0]*1.01,p1_file[5:12])
    print "%10.4f%10.5f%10.4f%10.5f" % (ave_xp, ave_yp, std_xp, std_yp)
    return id, ave_xp, std_xp, ave_yp, std_yp

def outline():
    xfs = sorted(glob.glob(options.xf))
    yfs = sorted(glob.glob(options.yf))
    assert len(xfs) == len(yfs), "the number of xyfs are not the same!!\n%r\n%r" % (xfs, yfs)
    fig = plt.figure(figsize=(12,9))
    ax = fig.add_subplot(1,1,1)
    xps, yps, ids, axes = {}, {}, [], [ax]
    for k, xyf in enumerate(zip(xfs,yfs)):
        print xyf
        id, ave_xp, std_xp, ave_yp, std_yp = ax_ave(xyf,ax)
        ids.append(id)
        xps[id] = [ave_xp-std_xp, ave_xp+std_xp]
        yps[id] = [ave_yp-std_yp, ave_yp+std_yp]
    ax.legend()
    q_acc.decorate(ids,xps,yps,axes,options)
    q_acc.show_or_save(options.of)
    
if __name__ == '__main__':
    import time; b = time.time()
    global options
    options = q_acc.parse_cmd()
    outline()
    e = time.time()
    print e - b

