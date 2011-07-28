#!/usr/bin/env python

import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
from xvg2png import xvg2array
from mpl_toolkits.axes_grid1.parasite_axes import SubplotHost
from seq_relevant_map import seq_map, char_map, col_map, chr_col_map

import pprint
smap = seq_map()
chmap = char_map()
comap = col_map()
ccmap = chr_col_map()

def get_coordinates(p1file,p2file):
    p1 = xvg2array(p1file)[1]
    p2 = xvg2array(p2file)[1]
    return p1, p2

def get_ave_std(p1file,p2file):
    """input files are those containing changes of property1,
    property2 along the trajectory""" 
    timep1, p1 = xvg2array(p1file)
    timep2, p2 = xvg2array(p2file) # timep1 & timenp2 will not be used, just for assignment
    p1 = [np.average(p1), np.std(p1)]
    p2 = [np.average(p2), np.std(p2)]
    # p1_list & p2_list are lists containing [average of p1, standard error of p2]
    return p1, p2

def _plot(p1_infiles,p2_infiles2,bottom_label,left_label,tau_b=1000):
    fig = plt.figure(figsize=(12,9))
    ax = fig.add_subplot(111)
    for p1f, p2f in zip(p1_infiles,p2_infiles):
        p1, p2 = get_coordinates(p1f, p2f)
        print len(p1), len(p2)
        bi = p1f.find('sq'); id = p1f[bi:bi+4]
        ax.plot(p1,p2,ccmap[id],markersize=5, alpha=0.2)
        # for i, j in zip(p1[::10],p2[::10]):

        #     dot = ax.plot(i,j, ccmap[id], markersize=5)
    ax.set_xlabel(bottom_label)
    ax.set_ylabel(left_label)
    ax.set_xlim(lims[bottom_label])
    ax.set_ylim(lims[left_label])
    ax.grid(b=True)
    plt.show()
    # plt.savefig('cluster_%s_%s_%s.png' % (id,left_label,bottom_label))

if __name__ == '__main__':
    """please also specify the properties you are gonna plot
    against, e.g. npi & hbnum,
    sys.argv[1]: p1 files; please use quotes
    sys.argv[2]: p2 files
    sys.argv[3]: bottom label, corresponding to p1
    sys.argv[4]: left label, corresponding to p2
    """
    lims = {
        'hbpp' : [0,40],
        'hbps' : [0,120],
        'gyr'  : [0,3.0],
        'npi'  : [0,150]
        }
    p1_infiles = sorted(glob.glob('%s' % sys.argv[1]))
    p2_infiles = sorted(glob.glob('%s' % sys.argv[2]))
    print p1_infiles
    print p2_infiles
    bottom_label = sys.argv[3]
    left_label = sys.argv[4]
    _plot(p1_infiles,p2_infiles,bottom_label,left_label)

