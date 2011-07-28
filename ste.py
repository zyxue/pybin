#!/usr/bin/env python
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from xvg2png import xvg2array
from det_row_col import det_row_col

"""
Author: Zhuyi Xue zhuyi.xue@utoronto.ca

this script will be used directly, no import necessary
to see which block size will be appropriate when calculating block averaging
"""

def prepare_ste_data(data,min_tau_b=1,max_tau_b=2000,stride=50,sflag=False):
    """
    tau_p is the block size, this module will plot the change of standard errors
    as tau_p increse.

    If sflag is True, the change of s will be plotted against tau_p in stead of
    standard errors 

    data should be in the type of numpy array
    """
    len_data = len(data)
    stes = []                                          # list of standard errors
    tau_bs = range(min_tau_b,max_tau_b,stride)         # list of tau_b
    ses = []                                           # s = tau_b * np.std(block_aves)**2 / (np.std(y))**2
    for tau_b in tau_bs:                               # tau_b: block siz
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
        if not sflag:                   # when sflag is False, not sflag is True
            s  = tau_b * np.std(block_aves)**2 / (np.std(data))**2
            ses.append(s)
        else:
            ste  = np.std(block_aves)
            stes.append(ste)
    if not sflag: return tau_bs, ses
    else: return tau_bs, stes

def inte_ste_data(infiles):
    """
    To store standard error data as in a nested list, also obtain the minmum
    and maximum of y, which will be used as the ylim
    """
    data_dict = {}
    ymines = []                          
    ymaxes = []                          # maxes are used to determine the y_lim
    for infile in infiles:
        data = xvg2array(infile)[1]
        x, y = prepare_ste_data(data,min_tau_b,max_tau_b,stride,sflag)
        data_dict[infile] = [x,y]
        ymines.append(min(y))
        ymaxes.append(max(y))
    return data_dict, min(ymines), max(ymaxes)

def quickplot(key,x,y,ymin,ymax,ax):
    """
    additional decorations to each subplot could be done here
    """
    if not sflag:                                                # sflag = False
        ax.plot(x,y,"ro",linewidth=1)
    else:
        ax.plot(x,y,"b-")
    ax.set_title(key)
    ax.set_ylim([ymin*0.9,ymax*1.1])
    ax.grid()

def subplots(infiles):
    fig = plt.figure()
    len_infiles = len(infiles)
    row,col = det_row_col(len_infiles)
    data_dict, ymin, ymax = inte_ste_data(infiles)
    ks = range(len_infiles)
    for key, k in zip(sorted(data_dict.keys()),ks):
        ax = fig.add_subplot(row,col,k+1)
        x,y = data_dict[key]
        quickplot(key,x,y,ymin,ymax,ax)
    plt.show()


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog -f FILES [-bes] [--sflag]", version="%prog 1.0")
    parser.add_option("-f", "--files", action="store", type="str", dest="files",
                      help="data files")
    parser.add_option("-b", "--min_tau_b",action="store",type="int",dest="min_tau_b",default=1,
                      help="the first index of your data, be careful with how many number of data you have")
    parser.add_option("-e", "--max_tau_b",action="store",type="int",dest="max_tau_b",default=200,
                      help="the ending")
    parser.add_option("-s", "--stride",action="store",type="int",dest="stride",default=50,
                      help="the stride")
    parser.add_option("--sflag", action="store_true",dest="sflag",default="False",
                      help="sflag True or False, when specified -sflag, it's True")
    (options, args) = parser.parse_args()
    args.insert(0,options.files); infiles = args
    min_tau_b=options.min_tau_b
    max_tau_b=options.max_tau_b
    stride = options.stride
    sflag = options.sflag
    print sflag
    subplots(infiles)
