#! /usr/bin/env python

import sys

import numpy as np
import tables

import argparse_action as aa
from mysys import read_mysys
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

def loop_h5_ave(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, ave_kwargs):
    mysys = read_mysys.read()
    for seq in SEQS:
        dd = {                                 # ppty_name: [denominator, interested_col]
        'dssp_E': [float(mysys[seq].len), 'structure'],
        'dssp_H': [float(mysys[seq].len), 'structure'],
        'dssp_G': [float(mysys[seq].len), 'structure'],
        'dssp_B': [float(mysys[seq].len), 'structure'],
        'dssp_C': [float(mysys[seq].len), 'structure'],
        'dssp_T': [float(mysys[seq].len), 'structure'],
        'upup'  : [float(mysys[seq].hbg), 'upup' ],
        'unun'  : [float(mysys[seq].scnpg * 2),'unun'], # g_mindist_excl1 double counts the contact, so divided by 2
        'upun'  : [1., 'upun'],
        'upvp'  : [float(mysys[seq].hbg), 'upvp' ],
        'upvn'  : [float(mysys[seq].hbg), 'upvn' ],
        'unvp'  : [float(mysys[seq].scnpg), 'unvp' ],
        'unvn'  : [float(mysys[seq].scnpg), 'unvn' ],
        'rg_c_alpha': [1., 'rg'],
        'rg_whole_length': [1., 'rg'],
        'rg_backbone': [1., 'rg'],
        'e2ed': [1., 'e2ed'],
        }
        for cdt in CDTS:
            dd['upv'] = [float(mysys[seq + cdt].nm_upv), 'upv' ]

            tablename = ave_kwargs['tablenamepattern'].format(seq=seq, cdt=cdt)
            if tpostproc_group.__contains__(tablename):
                print "{0} HAS ALREADY EXISTED".format(tablename)
                pass
            else:
                # prepare for creating a new table
                denominator, interested_col = dd[ppty]
                pfpattern = ave_kwargs['pfpattern']

                aves = []
                for num in NUMS:
                    pf = pfpattern.format(**locals())
                    if h5file.root.ogd.__contains__(pf):
                        t = h5file.getNode(h5file.root.ogd, pf)
                        v = t.read(field=interested_col).mean()
                        v_normed = v / denominator
                        aves.append(
                            (pf, v_normed.mean(), v_normed.std()) # append a tuple
                            )
                    else:
                        print "{0} doesn't exist in ogd, YOU KNOW THAT, RIGHT?".format(pf)

                t = h5file.createTable(
                    tpostproc_group._v_pathname, tablename, tave, title=(
                        'average value of {0} of {1} replica normded by {2}'.format(ppty, len(NUMS), denominator)))
                t.append(aves)
                print "{0} IS DONE".format(tablename)
    h5file.close()

def loop_h5_alx(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, alx_kwargs):
    mysys = read_mysys.read()

    arrayname_pattern = alx_kwargs['arraynamepattern']

    for seq in SEQS:
        dd = {                       # ppty_name: [denominator, x_col, y_col]
            'rg_c_alpha' : [1, 'time', 'rg_c_alpha'],
            'dssp_E'     : [float(mysys[seq].len), 'time', 'structure'],
            'conf_entropy' : [1, 'time', 'entropy'],
            # 'sequence_spacing' : ['dij', 'ave_d'],
            # 'rdf_upup': ['radius', 'rdf'],
            # 'rdf_upun': ['radius', 'rdf'],
            # 'rdf_unun': ['radius', 'rdf'],
            # 'rdf_upvp': ['radius', 'rdf'],
            # 'rdf_upvn': ['radius', 'rdf'],
            # 'rdf_unvp': ['radius', 'rdf'],
            # 'rdf_unvn': ['radius', 'rdf'],

            'rdf_un1vn': [1, 'radius', 'rdf'],
            'rdf_un2vn': [1, 'radius', 'rdf'],
            'rdf_un3vn': [1, 'radius', 'rdf'],
            'rdf_un1vp': [1, 'radius', 'rdf'],
            'rdf_un2vp': [1, 'radius', 'rdf'],
            'rdf_un3vp': [1, 'radius', 'rdf'],

            'rdf_c1vn': [1, 'radius', 'rdf'],
            'rdf_c2vn': [1, 'radius', 'rdf'],
            'rdf_c3vn': [1, 'radius', 'rdf'],
            'rdf_c1vp': [1, 'radius', 'rdf'],
            'rdf_c2vp': [1, 'radius', 'rdf'],
            'rdf_c3vp': [1, 'radius', 'rdf'],

            'rg_whole_length': [1., 'time', 'rg'],

            }
        for cdt in CDTS:
            arrayname = arrayname_pattern.format(seq=seq, cdt=cdt)
            if tpostproc_group.__contains__(arrayname):
                pass
            else:
                denominator, xcoln, ycoln = dd[ppty]      # xcol, ycol name, respectively
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
                raise ValueError(
                    "ref: {0} and {1} have different x axes".format(t_ref, t.name)
                    )
    return min_xlen, xaxis_ref
