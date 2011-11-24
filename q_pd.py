#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.patches as patches
import matplotlib.path as path
import glob
from optparse import OptionParser
from xvg2png import xvg2array
from det_row_col import det_row_col
from Mysys import read_mysys_dat
from q_cluster import det_lim

"""pd: probability distribution"""


mysys = read_mysys_dat()

def ax_distri(id,n,b,xlim,ylim,xlb,ylb,ax):
    left = np.array(b[:-1])                     
    right = np.array(b[1:])
    bottom = np.zeros(len(left))
    top = bottom + n                                  # n has alread been normed in gen_nbs() 
    XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T # not completely understand the math behide this line
    barpath = path.Path.make_compound_path_from_polys(XY)               # veried the correctness on April 2nd
    patch = patches.PathPatch(barpath,fill=False,edgecolor=mysys[id].col,alpha=1,hatch='\\',label=mysys[id].seq)
    ax.add_patch(patch)
    ax.set_label(mysys[id].seq)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(b=True)
    ax.legend(loc='best')
    # ax.set_xlim(left[0], right[-1])
    # ax.set_ylim(bottom.min(), top.max())

def gen_nbs(infs,bins):         # nbs: collections of n and bins
    ns = {}                     # collection of n, containing the number of bins
    bs = {}                     # collection of bins
    ids = []
    for inf in infs:
        bi = inf.find('sq'); id = inf[bi:bi+4]; ids.append(id)
        y = xvg2array(inf)[1]
        print inf
        n, b = np.histogram(y,bins,normed=False) # if Normed=True, the results will be distribution density
        ns[id] = n / float(len(y))
        # normed by the total number of data points, so the plot result is probability
        # distribution function instead of distribution density
        bs[id] = b
    return ids, ns, bs

def outline(infs, options):
    fig = plt.figure(figsize=(24,11.6625))
    l = len(infs)
    row,col = det_row_col(l)
    ids, ns, bs = gen_nbs(infs,options.bins)
    xlim = [options.xb,options.xe] if options.xb!=None and options.xe!=None else det_lim(ids,bs)
    ylim = [options.yb,options.ye] if options.yb!=None and options.ye!=None else det_lim(ids,ns)
    xlb = options.xlb if options.xlb else 'x'
    ylb = options.ylb if options.ylb else 'y'
    for k, id in enumerate(ids):
        ax = fig.add_subplot(row,col,k+1)
        ax_distri(id,ns[id],bs[id],xlim,ylim,xlb,ylb,ax)
    plt.show()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f',type='str',dest='fs',help='specify the data files')
    parser.add_option('--xlb',type='str',default=None,dest='xlb',help='bottom label')
    parser.add_option('--ylb',type='str',default=None,dest='ylb',help='left label')
    parser.add_option('--xb',type='float',default=None,dest='xb',help='specifly x beginning')
    parser.add_option('--xe',type='float',default=None,dest='xe',help='specifly x ending')
    parser.add_option('--yb',type='float',default=None,dest='yb',help='specifly y beginning')
    parser.add_option('--ye',type='float',default=None,dest='ye',help='specifly y ending')
    parser.add_option('--bins',type='int',default=10,dest='bins',help='specify the number of bins')
    options, args = parser.parse_args()
    infs = sorted(glob.glob(options.fs))
    # start plotting
    import time; b = time.time()
    outline(infs,options)
    e = time.time()
    print e - b

