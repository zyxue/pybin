#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import sys
import glob
from mpl_toolkits.axes_grid1 import ImageGrid
from Process_grofile import Process_grofile
from q_cluster import parse_cmd
from Mysys import read_mysys_dat
from gen_hblist import gen_hblist

mysys = read_mysys_dat()

def calc_turn(turn_hblist,diff=3):
    """
    turn_hblist could be generate using gen_hblist.py module. Three input files
    are necessary, one is gro file, the other two could be generated by g_hbond
    with -hbn -hbm options
    
    with difference diff parameter, difference types of turns could be
    calculated, default is 4, which corresponds to beta turns. e.g. 
    diff = 5: pi turn
    diff = 4: alpha turn
    diff = 3: beta turn
    diff = 2: gamma turn
    diff = 1: delta turn
    negative diff corresponding to reversed turns 
    """
    fb_turn = []                                            # forward beta turn
    rb_turn = []                                            # reversed beta turn
    for hb in turn_hblist:
        d = hb[0]-hb[1]
        if d == 3: # the NH of i+3th residue forms hbond with C=O of ith residue
            fb_turn.append(hb)
        elif d == -3:
            rb_turn.append(hb)
    import copy
    turn = copy.copy(fb_turn)
    turn.extend(rb_turn)                             # combine fb_turn & rb_turn
    # Here I just write the code that regardless of forward or reversed turns,
    # later this piece should be imporved so as to distinguish fb_turn and
    # rb_turn
    tnum_list = [] # turn num list: used to collect the number of turn of each frame
    fnum = len(turn[0][2])                             # num is the frame number
    for k in range(fnum):
        counter = 0
        for hb in turn:
            if hb[2][k] == 'o': # hb[2] is the line with label "o" or space for every frame
                counter += 1
        tnum_list.append(counter)
    return tnum_list

def calc_all_turns(hblist,diff=[1,2,3,4,5,6,7],frflag=False):
    """
    hblist could be generate using gen_hblist.py module. Three input files
    are necessary, one is gro file, the other two could be generated by g_hbond
    with -hbn -hbm options

    It is a list nested list of sublists:
    ["resid_of N", "resid of CO", "the line with label "o" or space for every hbpair"]
    
    this function is different from calc_turn since it will include all kinds of
    turns as listed above by default: alpha, beta, gamma, delta & pi, no matter
    forward or reversed. You could modified diff parameter to exclude certain
    kinds of turns, frflag is for future if the user wanna distinguish forward
    and reversed turns
    """
    turn_data = []                                 # used to filter hblist, collect those that for turns
    for hb in hblist:
        if abs(hb[0]-hb[1]) in diff:
            turn_data.append(hb)
    # start counting for each frame
    fs = len(hblist[0][2]) # the frame number, but frame is not the time here!!
    turns = []             # in the same order with fs
    for k in range(fs): 
        counter = 0                                # turn counter for each frame
        for hb in hblist:
            if hb[2][k] == 'o': # hb[2] is the line with label "o" or space for every frame
                counter += 1
        turns.append(counter)
    return turns

def write_turns(turns,outputfile,xvgfile=None):
    """ input turn is a list in the order of frame number, data will be written
    in a xvg format"""
    if xvgfile:
        from xvg2png import xvg2array
        times = xvg2array(xvgfile)[0]
    else:
        times = range(turns) + 1                 # starting from 1,2,3,4,5,6....
    assert len(times) == len(turns), "the index of frames is not right"
    with open(outputfile,'w') as opf:
        for time, turn in zip(times, turns): # xvgfile is not specified, then times == turns.keys(), is the frame index
            opf.write("%-20g%-10g\n" % (time,turn))

if __name__ == "__main__":
    """ Usage: e.g. 
    cal_turns.py -f "*.xvg" --ndx "*.ndx" --gro "*gro" --xpm "*.xpm"
    at the directory where those files are located, then copy move to other places
    """
    options = parse_cmd()
    xpmfiles = sorted(glob.glob(options.xpm))
    grofiles = sorted(glob.glob(options.gro))
    ndxfiles = sorted(glob.glob(options.ndx))
    xvgfiles = sorted(glob.glob(options.fs))
    print len(xpmfiles), len(grofiles), len(ndxfiles),len(xvgfiles)
    for ndxf, grof, xpmf, xvgf in zip(ndxfiles,grofiles,xpmfiles,xvgfiles):
        print ndxf, grof, xpmf, xvgf
        hblist = gen_hblist(ndxf, grof, xpmf)
        turns = calc_all_turns(hblist)
        groinfo = Process_grofile(grof)
        write_turns(turns, "%s_turn.xvg" % xpmf[:10],xvgf)
