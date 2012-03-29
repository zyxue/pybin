#! /usr/bin/env python

import os
import argparse

import tables
import numpy as np
from configobj import ConfigObj

from common_func import get_sctn
from mysys import read_mysys

from common import tave, parse_cmd

def main():
    args = parse_cmd()

    # initialization YOU DIAN LUANG!

    conf = args.conf
    if not os.path.exists(conf):
        raise IOError("{0} cannot found".format(conf))

    conf_dict = ConfigObj(conf)
    SEQS, CDTS, TMPS, NUMS = get_sctn(args, conf_dict['systems'])

    h5filename = conf_dict['data']['h5filename']
    if not os.path.exists(h5filename):
        raise IOError("{0} cannot found".format(h5filename))

    ppty = args.ppty
    tpostproc='alx'                               # type of postprocess. i.e. ave

    alx_kwargs = conf_dict['postprocess'][tpostproc]

    rootUEP = os.path.join('/', args.ppty)

    # start dealing with the h5 file
    h5file = tables.openFile(h5filename, 'a', rootUEP=rootUEP)

    tpostproc_group_path = os.path.join('/', tpostproc)
    if h5file.__contains__(tpostproc_group_path):
        tpostproc_group = h5file.getNode(h5file.root, tpostproc)
    else:
        tpostproc_group = h5file.createGroup(h5file.root, tpostproc)

    loop_h5_alx(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, alx_kwargs)

def loop_h5_alx(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, alx_kwargs):
    mysys = read_mysys.read()

    arrayname_pattern = alx_kwargs['arraynamepattern']

    for seq in SEQS:
        dd = {                       # ppty_name: [denominator, interested_col]
            'rg_c_alpha' : ['time', 'rg_c_alpha'],
            'sequence_spacing' : ['dij', 'ave_d'],
            'rdf_upup': ['radius', 'rdf'],
            'rdf_upun': ['radius', 'rdf'],
            'rdf_unun': ['radius', 'rdf'],
            'rdf_upvp': ['radius', 'rdf'],
            'rdf_upvn': ['radius', 'rdf'],
            'rdf_unvp': ['radius', 'rdf'],
            'rdf_unvn': ['radius', 'rdf']
            }
        for cdt in CDTS:
            arrayname = arrayname_pattern.format(seq=seq, cdt=cdt)
            if tpostproc_group.__contains__(arrayname):
                pass
            else:
                xcoln, ycoln = dd[ppty]      # xcol, ycol name, respectively
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
                        
                # starting to collect vales along the y axis
                ave_ds = []                                 # ave distances
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
                                'ref: {0} and {1} have different x axes'.format(t_ref, t.name)
                                )
                        else:
                            ave_ds.append(table.read(field=ycoln))

                ave_ds = np.array(ave_ds)
                alx_ave = np.average(ave_ds, axis=0)       # summing along the 0th axis
                alx_std = np.std(ave_ds, axis=0)
                # from scipy import stats
                # alx_std = stats.sem(ave_ds, axis=0)

                # if np.array(alx_index_ref) in previously code, comparing two arrays raise complexity
                # alx_index = np.array(alx_index_ref)

                # transpose to be in consistend with tables in ogd
                alx_result = np.array([xaxis_ref, alx_ave, alx_std]).transpose()
                array = h5file.createArray(
                    tpostproc_group, arrayname, alx_result, 
                    title=('average along the x axis over all replicas'
                           'column 0, 1, 2 are x axis, ave, std, respectively'))
            print arrayname
    h5file.close()

if __name__ == "__main__":
    main()

