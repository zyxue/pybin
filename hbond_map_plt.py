#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import sys
from mpl_toolkits.axes_grid1 import ImageGrid
from Process_grofile import Process_grofile

def gen_hblist_index(hbnfile):
    infile = open(hbnfile, 'r')
    for line in infile:        
        if line.startswith('[ hbonds'):
            break
    hblist_index = []
    for line in infile:
        split_line = line.split()
        hblist_index.append([int(split_line[0]),int(split_line[2])])
    return hblist_index # in the form of nested [index_of_N, index_of_O]

def gen_hblist_resid(grofile, hbnfile):
    """replace index in the hblist_index with resid"""
    hblist_resid = gen_hblist_index(hbnfile)
    groinfo = Process_grofile(grofile)
    pl = groinfo.pl()
    for k, hbpair in enumerate(hblist_resid):
        hblist_resid[k][0] = groinfo.resid(hbpair[0])
        hblist_resid[k][1] = groinfo.resid(hbpair[1])
    return hblist_resid, pl
    # Now we have got the nested hblist_resid with each sublist
    # [resid_of_N, resid_of_dCO]

    # Now we need to count the number of "o" in each line of the matrix
def gen_final_hblist(xmpfile,grofile,hbnfile):
    final_hblist, pl = gen_hblist_resid(grofile, hbnfile)
    final_hblist.reverse()      # so that we could use the xpm file upside down    
    reversed_lines = reversed(open(xmpfile, 'r').readlines())
    for i, line in enumerate(reversed_lines):
        if line.startswith('"'):
            final_hblist[i].append(line.count('o') / float(len(line)-4)) 
            # 4 represents "",\n in a line
            # append the probablities of hbonds
        else:
            break
    return final_hblist, pl
    # Now we have got the nested final_hblist with each sublist
    # [resid_of N, resid of CO, probability_of_hbond, ]

def figure_grid(nrows=1, ncols=1):
    F = plt.figure(1,(23,10))
    grid = ImageGrid(F, 111, # similar to subplot(111) #not quite understand 2011/01/03
                     nrows_ncols = (nrows,ncols),
                     axes_pad = 0.3,
                     add_all=True,
                     label_mode = "L",
                     )
    return grid

def hbmap_plot(hblist,pl):
    data = np.zeros((pl,pl))
    for sublist in hblist:
        data[sublist[0]-1][sublist[1]-1] = sublist[2]
    ax = figure_grid()[0]
    im = ax.imshow(data, origin="lower", cmap="Paired",      # cmap could also be Greys
                   vmin=0, vmax=1,interpolation="nearest")
    ax.grid()
    ax.set_xlabel('C')
    ax.set_ylabel('N')
    plt.colorbar(im)
    plt.show()

if __name__ == "__main__":
    """We need
    sys.argv[1]: xmpfile,
    sys.argv[2]: grofile,
    sys.argv[3]: ndxfile -hbn output
    """
    hblist,pl = gen_final_hblist(sys.argv[1], sys.argv[2], sys.argv[3])
    print pl
    hbmap_plot(hblist,pl)
