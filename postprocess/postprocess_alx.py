#! /usr/bin/env python

import os

import tables
import numpy as np
from configobj import ConfigObj

from common_func import tave, parse_cmd
from mysys import read_mysys

def main():
    mysys = read_mysys.read()

    args = parse_cmd()
    conf_dict = ConfigObj(args.conf)
    h5file = args.h5f
    UEP = args.ppty
    topproc = 'alx'

    rootUEP = os.path.join('/', UEP)
    h5f = tables.openFile(h5file, 'a', rootUEP=rootUEP)

    path = os.path.join('/', topproc)
    print path

    if h5f.__contains__(path):
        g = h5f.getNode(h5f.root, topproc)
    else:
        g = h5f.createGroup(h5f.root, topproc)
    print g

    SEQS = conf_dict['systems']['SEQS']
    CDTS = conf_dict['systems']['CDTS']
    NUMS = conf_dict['systems']['NUMS']

    arrayname_pattern = conf_dict['postprocess'][topproc]['arraynamepattern']

    for seq in SEQS:
        for cdt in CDTS:
            arrayname = arrayname_pattern.format(seq=seq, cdt=cdt)
            if g.__contains__(arrayname):
                pass
            else:
                # prepare for creating a new table
                dd = {
                    'sequence_spacing' : ['dij', 'ave_d'],
                    'rdf_upup': ['radius', 'rdf'],
                    'rdf_upun': ['radius', 'rdf'],
                    'rdf_unun': ['radius', 'rdf'],
                    'rdf_upvp': ['radius', 'rdf'],
                    'rdf_upvn': ['radius', 'rdf'],
                    'rdf_unvp': ['radius', 'rdf'],
                    'rdf_unvn': ['radius', 'rdf']
                    }
                pfpattern = conf_dict['postprocess'][topproc]['pfpattern']
                xcoln, ycoln = dd[UEP]      # xcol, ycol name, respectively
                    
                ts = [h5f.getNode(h5f.root.ogd, pfpattern.format(
                            seq=seq, cdt=cdt, num=num)) for num in NUMS
                      ]                                 # collect tables in ogd

                ave_ds = []                                 # ave distances
                ftflag = True                               # first table flag
                for t in ts:
                    if ftflag:
                        t_ref = t.name
                        alx_index_ref = [x[xcoln] for x in t.iterrows()]
                        ftflag = False
                    else:
                        print alx_index_ref
                        if [x[xcoln] for x in t.iterrows()] != alx_index_ref:
                            raise ValueError(
                                'ref: {0} and {1} have difference x axes'.format(t_ref, t.name)
                                )
                        else:
                            ave_ds.append([x[ycoln] for x in t.iterrows()])

                ave_ds = np.array(ave_ds)
                alx_ave = ave_ds.mean(axis=0)       # summing along the 0th axis
                alx_std = ave_ds.std(axis=0)

                # if np.array(alx_index_ref) in previously code, comparing two arrays raise complexity
                alx_index = np.array(alx_index_ref)

                # transpose to be in consistend with tables in ogd
                alx_result = np.array([alx_index, alx_ave, alx_std]).transpose()
                array = h5f.createArray(
                    g, arrayname, alx_result, title=\
                    'average along the x axis over all replicas, column 0, 1, 2 are x axis, ave, std, respectively')
    h5f.close()

if __name__ == "__main__":
#     h5file = '../mono_meo.h5'
#     topproc = 'alx'
#     UEP = 'sequence_spacing'
    main()

