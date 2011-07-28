#!/usr/bin/env python

import sys

import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from q_acc import parse_cmd
from Mysys import read_mysys_dat
from pprint import pprint as pp
import q_acc

mysys = read_mysys_dat()

""" it's slow, could be improved a lot 2011-04-04"""

def get_data(inf):
    for line in inf:
        if (not line.startswith('#') and 
            not line.startswith('@') and
            line.strip()):
            yield [ float(i) for i in line.strip().split()[:2] ]

def calc_secondary_structures(inf):
    lines = np.array(list(get_data(inf)))
    psi = lines[:,0]
    phi = lines[:,1]
    h, phip, psip = np.histogram2d(phi, psi, range=[[-180,180], [-180,180]],
                                   bins=36)
    return h, phip, psip

def outline(options):
    infile = glob.glob(options.fs)[0]
    with open(infile, 'r') as inf:
        h, phip, psip = calc_secondary_structures(inf)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    contour = ax.contourf(phip[1:], psip[1:], h, cmap=cm.gray_r)
    ax.set_title(infile)
    plt.colorbar(contour, shrink=0.6, extend='both')
    q_acc.show_or_save(options.of)

if __name__ == '__main__':
    """Usage: e.g.
    rama2pp2.py -f "*rama.xvg"
    operating in the directory where *ramra.xvg files are
    """    
    options = q_acc.parse_cmd()
    outline(options)
    # infiles = sorted(glob.glob(parse_cmd().fs))
    # for inf in infiles:
    #     print inf
    #     rama2pp2(inf)
