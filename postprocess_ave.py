#! /usr/bin/env python

import os

import tables
import numpy as np
from configobj import ConfigObj

from mysys import read_mysys

class tave(tables.IsDescription):
    """table ave"""
    pf = tables.StringCol(itemsize=15, pos=0)    # like an unique id                     
    ave = tables.Float32Col(pos=1)
    std = tables.Float32Col(pos=2)

# Modulize the code, and plot upup V.S. dssp_E

def main(h5file, UEP, topproc):
    mysys = read_mysys.read()
    conf_dict = ConfigObj('.h5.conf')

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
    tablename_pattern = conf_dict['postprocess'][topproc]['tablenamepattern']

    for seq in SEQS:
        for cdt in CDTS:
            tablename = tablename_pattern.format(seq=seq, cdt=cdt)
            print tablename
            if g.__contains__(tablename):
                pass
            else:
                # prepare for creating a new table
                dd = {
                    'dssp_E': [float(mysys[seq].len), 'Structure'],
                    'upup'  : [float(mysys[seq].hbg), 'num_upup' ],
                    'unun'  : [float(mysys[seq].scnpg),'num_unun'],
                    'upun'  : [1., 'num_upun'],
                    'upvp'  : [float(mysys[seq].hbg), 'num_upvp' ],
                    'upvn'  : [float(mysys[seq].hbg), 'num_upvn' ],
                    'unvp'  : [float(mysys[seq].scnpg), 'num_unvp' ],
                    'unvn'  : [float(mysys[seq].scnpg), 'num_unvn' ],
                    'rg_c_alpha': [1., 'rg_c_alpha']
                    }

                denorminator, interested_col = dd[UEP]

                pfpattern = conf_dict['postprocess'][topproc]['pfpattern']

                aves = []
                for num in NUMS:
                    pf = pfpattern.format(**locals())
                    t = h5f.getNode(h5f.root.ogd, pf)
                    v = np.array([x[interested_col] for x in t.iterrows()])
                    v_normed = v / denorminator
                    aves.append(
                        (pf, v_normed.mean(), v_normed.std()) # append a tuple
                        )

                t = h5f.createTable(
                    g, tablename, tave,
                    title=\
                    'average value of each replica for {0} normded by {1}'\
                    .format(UEP, denorminator))
                t.append(aves)
    h5f.close()

# I tried with append [str, float, float] to an array, then every element in
# the list will be converted to str, so not convenient for following
# analysis. Then, I choose to create a table instead of an array because I do
# need the pf to each row as an identity
if __name__ == "__main__":
    h5file = '../mono_meo.h5'
    topproc = 'ave'                                                  # type of postprocess. i.e. ave
    for UEP in ['unvp', 'upvp']:
        main(h5file, UEP, topproc)
