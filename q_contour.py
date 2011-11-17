#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import sys
import glob
from xvg2png import xvg2array_nt
import q_acc
from Mysys import read_mysys_dat

mysys = read_mysys_dat()

def make_continuous(data, dnorm=2): # dnorm: the denominator used to average the data
    """data should be 1D"""
    l = len(data)/dnorm
    for k in range(l):         # k is the length of the new data
        i = k*dnorm
        j = i + dnorm
        yield np.average(data[i:j])
    if len(data)%dnorm != 0:
        yield np.average(data[i+dnorm:])

def ax_contour(xyf,ax):
    xf, yf = xyf
    x_data = list(make_continuous(xvg2array_nt(xf), dnorm=10)) 
    y_data = list(make_continuous(xvg2array_nt(yf), dnorm=10))
    assert len(x_data) == len(y_data)
    h, xp, yp = np.histogram2d(x_data, y_data, bins=options.bins)
    h = h / float(len(x_data)) * 100.
    left, right, bottom, top = xp[0], xp[-1], yp[0], yp[-1]
    extent = [left,right,bottom,top]
    # im = ax.imshow(h, extent=extent,interpolation='bilinear',origin='lower',cmap=cm.gray_r, vmin=10, vmax=8000)
    levels = [ i/100. for i in range(10,400,40)]
    pid, sid = q_acc.get_id(xyf)
    cs = ax.contour(xp[1:]-(xp[1]-xp[0])/2.,
                    yp[1:]-(yp[1]-yp[0])/2., 
                    # make it align with imshow, shift a little since x, y are
                    # bins, the following line do the same thing
                    h,levels=levels,color=mysys[pid].col,extent=extent,origin='lower',
                    label=mysys[pid].seq+mysys[sid].cdt)
    # cs = ax.contour(x[:-1]+(x[1]-x[0])/2.,y[:-1]+(y[1]-y[0])/2,h)

    plt.clabel(cs, [levels[0],levels[1],levels[-1]],  # label every second level
               inline=1,
               fmt='%.2f',
               fontsize=8)
    ax.legend()
    # CBI = plt.colorbar(im, orientation='vertical', shrink=1)
    # zc = len(cs.collections)                                   # line collection
    # print zc
    # plt.setp(zc, linewpidth=4)

    # ax.set_title(mysys[pid].seq)
    # CB = plt.colorbar(cs, shrink=0.6, extend='both')
    # plt.flag()
    return pid+sid, xp, yp

def outline():
    xfs = sorted(glob.glob(options.xf))
    yfs = sorted(glob.glob(options.yf))
    assert len(xfs) == len(yfs), "the number of xyfs are not the same!!\n%r\n%r" % (xfs, yfs)
    l = len(xfs)

    if options.overlap:
        olp = options.overlap
        assert l % olp== 0, "the num of infiles are not even to do overlap"
        row,col = q_acc.det_row_col(l/olp, options.morer)
    else:
        olp = 1
        row,col = q_acc.det_row_col(l,options.morer)

    fig = plt.figure(figsize=(24,11))
    xps, yps, ids, axes = {}, {}, [], []
    for k, xyf in enumerate(zip(xfs,yfs)):
        print xyf
        if k % olp == 0:
            ax = fig.add_subplot(row,col,k/olp+1)
        id, xp, yp = ax_contour(xyf,ax)
        axes.append(ax)
        ids.append(id)
        xps[id], yps[id] = xp, yp
    q_acc.decorate(ids,xps,yps,axes,options)
    q_acc.show_or_save(options.of)

if __name__ == '__main__':
    import time; b=time.time()
    global options
    options = q_acc.parse_cmd()
    outline()
    e = time.time()
    print e - b
