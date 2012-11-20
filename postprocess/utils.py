#! /usr/bin/env python

import sys

import numpy as np
import tables

import argparse_action as aa
from setting import calc_ave_dd, calc_alx_dd
from xvg2h5 import h5tables


def parse_cmd(cmd=None):
    parser = aa.my_basic_parser()
    parser.add_argument('-p', '--property-name', type=str, dest='ppty', required=True,
                        help='you must specify the --property-name option from {0!r}'.format(h5tables.__tables__))
    parser.add_argument('-a', dest='tpostproc', required=True,
                        help='type of postprocess. e.g. ave, alx')
    parser.add_argument('-g', dest='conf', default=".h5.conf",
                        help='specify the configuration file')

    if cmd is None:
        cmd = sys.argv[1:]

    args = parser.parse_args(cmd)
    return args

class tave(tables.IsDescription):                           # table of average
    """table ave"""
    pf = tables.StringCol(itemsize=15, pos=0)               # like an unique id
    ave = tables.Float32Col(pos=1)
    std = tables.Float32Col(pos=2)

# class tdistr(tables.IsDescription):                         # use array for distribution
#     """table ave"""
#     pf = tables.StringCol(itemsize=15, pos=0) # like an unique id                     
#      = tables.Float32Col(pos=1)

def calc_averages(NUMS, pfpattern, h5file, interested_col, denominator, seq, cdt):
    aves = []                                         # average of each replica
    for num in NUMS:
        pf = pfpattern.format(seq=seq, cdt=cdt, num=num)
        if h5file.root.ogd.__contains__(pf):
            t = h5file.getNode(h5file.root.ogd, pf)
            v = t.read(field=interested_col).mean()
            v_normed = v / denominator
            # append a tuple
            aves.append((pf, v_normed.mean(), v_normed.std()))
        else:
            print "{0} doesn't exist in ogd, YOU KNOW THAT, RIGHT?".format(pf)
    return aves

def loop_h5_ave(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, ave_kwargs):
    for seq in SEQS:
        for cdt in CDTS:
            ave_dd = calc_ave_dd(seq, cdt)

            tablename = ave_kwargs['tablenamepattern'].format(seq=seq, cdt=cdt)
            if tpostproc_group.__contains__(tablename):
                print "{0} HAS ALREADY EXISTED".format(tablename)
                pass
            else:
                # prepare for creating a new table
                denominator, interested_col = ave_dd[ppty]
                pfpattern = ave_kwargs['pfpattern']
                # here useful keys in locals() include seq, cdt, etc.
                aves = calc_averages(NUMS, pfpattern, h5file, interested_col, denominator, seq=seq, cdt=cdt)

                t = h5file.createTable(
                    tpostproc_group._v_pathname, tablename, tave, title=(
                        'average value of {0} of {1} replica normded by {2}'.format(ppty, len(NUMS), denominator)))
                t.append(aves)
                print "{0} IS DONE".format(tablename)
    h5file.close()

def loop_h5_alx(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, alx_kwargs):
    arrayname_pattern = alx_kwargs['arraynamepattern']

    for seq in SEQS:
        alx_dd = calc_alx_dd(seq)
        for cdt in CDTS:
            arrayname = arrayname_pattern.format(seq=seq, cdt=cdt)
            if tpostproc_group.__contains__(arrayname):
                print "{0} HAS ALREADY EXISTED".format(arrayname)
                pass
            else:
                denominator, xcoln, ycoln = alx_dd[ppty]      # xcol, ycol name, respectively
                # pf is used to identify the tables in ogd
                pfpattern = alx_kwargs['pfpattern']

                # collect tables in ogd
                tables = []
                for num in NUMS:
                    pf = pfpattern.format(seq=seq, cdt=cdt, num=num) 
                    if h5file.root.ogd.__contains__(pf):
                        tables.append(h5file.getNode(h5file.root.ogd, pf))
                    else:
                        print "{0} doesn't exist, you know this? Right!".format(pf)

                # need to compare the axes first and at the same time get the
                # minimum length of all the data first, all could be done by
                # get_minimum_length function
                min_len, xaxis_ref = get_minimum_length(tables, xcoln)

                # starting to collect vales along the y axis
                ave_ds = []                                 # ave distances
                for table in tables:
                    distance = table.read(field=ycoln)[:min_len]
                    ave_ds.append(distance)

                ave_ds = np.array(ave_ds) / denominator
                alx_ave = np.average(ave_ds, axis=0)       # summing along the 0th axis
                # alx_std = np.std(ave_ds, axis=0)
                from scipy import stats
                alx_std = stats.sem(ave_ds, axis=0)

                # if np.array(alx_index_ref) in previously code, comparing two arrays raise complexity
                # alx_index = np.array(alx_index_ref)

                # transpose to be in consistend with tables in ogd
                alx_result = np.array([xaxis_ref, alx_ave, alx_std]).transpose()
                h5file.createArray(
                    tpostproc_group, arrayname, alx_result, 
                    title=('average along the x axis over all replicas'
                           'column 0, 1, 2 are x axis, ave, std, respectively'))
            print "{0} IS DONE".format(arrayname)
    h5file.close()

def get_minimum_length(tables, xcoln):
    ftflag = True                               # first table flag
    for table in tables:
        if ftflag:
            t_ref = table.name
            xaxis_ref = table.read(field=xcoln) # xaxis reference
            min_xlen = len(xaxis_ref)       # minimum length for x axis
            ftflag = False
        else:
            xaxis = table.read(field=xcoln) # xaxis reference
            if len(xaxis) < min_xlen:
                min_xlen = len(xaxis)
                xaxis_ref = xaxis
            if set(xaxis[:min_xlen]) != set(xaxis_ref):
                raise ValueError("ref: {0} and {1} have different x axes".format(t_ref, table.name))
    return min_xlen, xaxis_ref
