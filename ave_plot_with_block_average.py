#!/usr/bin/env python

import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
from xvg2png import xvg2array
from mpl_toolkits.axes_grid1.parasite_axes import SubplotHost

"""
this module could be used directly, but the current directory would better to be
in the relative directory, so that the
        ax_host.text(p1[0]*1.02,p2[0]*1.02,p1_file[:7])
will make sense
"""

def block_average(data,tau_b):
    """
    calculate the block average with a block size of tau_b
    """
    len_data = len(data)
    block_aves = []
    block = []
    counter = 0
    while counter < len_data:
        block.append(data[counter])
        counter += 1
        if len(block) == tau_b:
            block_aves.append(np.average(block))
            block = []
        if counter == len_data and len(block) != 0: # include those data that are not enough to fill one block at last     
            block_aves.append(np.average(block))
    ste = np.std(block_aves)                               # ste: standard error
    return ste
    
def get_ave_ste(p1f,p2f,tau_b):
    """input files are those containing changes of property1,
    property2 along the trajectory""" 
    timep1, p1 = xvg2array(p1f)
    timep2, p2 = xvg2array(p2f) # timep1 & timenp2 will not be used, just for assignment
    p1_list = [np.average(p1), block_average(p1,tau_b)]
    p2_list = [np.average(p2), block_average(p2,tau_b)]
    # p1_list & p2_list are lists containing [average of p1, standard error of p2]
    return p1_list, p2_list

def _verify():
    """
    need repair
    """
    p1, p2 = get_ave_ste('verify1.txt','verify2.txt',tau_b=2)
    """write verify1.txt','verify2.txt"""
    ax_kms.errorbar(p1[0],p2[0], xerr=p1[1], yerr=p2[1],label='system')
    ax_kms.axis["bottom"].set_label("p1")
    ax_kms.axis["left"].set_label("p2")
    plt.legend()
    plt.show()

def _plot(p1_infiles,p2_infiles2,bottom_label,left_label,tau_b=1000):
    fig = plt.figure(figsize=(12,9))
    ax_host = SubplotHost(fig, 1,1,1)
    fig.add_subplot(ax_host)
    for p1_file, p2_file in zip(p1_infiles,p2_infiles):
        p1, p2 = get_ave_ste(p1_file, p2_file, tau_b=1000)
        ax_host.errorbar(p1[0],p2[0], xerr=p1[1], yerr=p2[1],label=p1_file[:4])
        ax_host.text(p1[0]*1.02,p2[0]*1.02,p1_file[:7])
    ax_host.axis["bottom"].set_label(bottom_label)
    ax_host.axis["left"].set_label(left_label)
    ax_host.grid()
    # if wanna legend, uncomment the following line
    # plt.legend()
    plt.show()
    

if __name__ == '__main__':
    """please also specify the properties you are gonna plot
    against, e.g. npi & hbnum,
    sys.argv[1]: p1 files; please use quotes
    sys.argv[2]: p2 files
    sys.argv[3]: bottom label, corresponding to p1
    sys.argv[4]: left label, corresponding to p2
    sys.argv[5]: tau_b
    """
    p1_infiles = sorted(glob.glob('%s' % sys.argv[1]))
    print p1_infiles
    p2_infiles = sorted(glob.glob('%s' % sys.argv[2]))
    print p2_infiles
    bottom_label = sys.argv[3]
    left_label = sys.argv[4]
    # tau_b = int(sys.argv[5])
    _plot(p1_infiles,p2_infiles,bottom_label,left_label)
