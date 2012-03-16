#! /usr/bin/env python

import os

import tables
import numpy as np
from configobj import ConfigObj

from mysys import read_mysys
from common_func import tave, parse_cmd

# Modulize the code, and plot upup V.S. dssp_E

def main(h5file, UEP, topproc):
    mysys = read_mysys.read()

    args = parse_cmd()
    conf_dict = ConfigObj('.h5.conf')
    
    h5file = args.h5f
    UEP = args.ppty
    topproc = 'distr'                           # type of postprocess. i.e. ave

    rootUEP = os.path.join('/', UEP)
    h5f = tables.openFile(h5file, 'a', rootUEP=rootUEP)

    path = os.path.join('/', topproc)
    print path

    if h5f.__contains__(path):
        g = h5f.getNode(h5f.root, topproc)
    else:
        g = h5f.createGroup(h5f.root, topproc)
    print g

    SEQS = conf_dict['systems']['SEQS'] if not 
    CDTS = conf_dict['systems']['CDTS']
    NUMS = conf_dict['systems']['NUMS']
    arrayname_pattern = conf_dict['postprocess'][topproc]['arraynamepattern']

    for seq in SEQS:
        for cdt in CDTS:
            arrayname = arrayname_pattern.format(seq=seq, cdt=cdt)
            print arrayname
            if g.__contains__(arrayname):
                pass
            else:
                if UEP == 'rg_c_alpha':
                    interested_col = 'rg_c_alpha'
                pfpattern = conf_dict['postprocess'][topproc]['pfpattern']

                distr = []                       # used to collect every points
                for num in NUMS:
                    pf = pfpattern.format(**locals())
                    t = h5f.getNode(h5f.root.ogd, pf)
                    v = np.array([x[interested_col] for x in t.iterrows()])
                    distr.extend(v)

                distr = np.array(distr)
                ar = h5f.createArray(
                    g, arrayname, distr, title=\
                    'collection of all the data points')
    h5f.close()

if __name__ == "__main__":
    h5file = '../mono_meo.h5'

    UEP = 'rg_c_alpha'
    main(h5file, UEP, topproc)
