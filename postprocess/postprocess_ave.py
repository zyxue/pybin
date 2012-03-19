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
    tpostproc='ave'                               # type of postprocess. i.e. ave

    ave_kwargs = conf_dict['postprocess'][tpostproc]

    rootUEP = os.path.join('/', ppty)
    # start dealing with the h5 file
    h5file = tables.openFile(h5filename, 'a', rootUEP=rootUEP)

    tpostproc_group_path = os.path.join('/', tpostproc)
    if h5file.__contains__(tpostproc_group_path): # means first time running ave postprocess for this ppty
        tpostproc_group = h5file.getNode(h5file.root, tpostproc)
    else:
        tpostproc_group = h5file.createGroup(h5file.root, tpostproc)

    loop_h5(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, ave_kwargs)

def loop_h5(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, ave_kwargs):
    mysys = read_mysys.read()
    for seq in SEQS:
        dd = {                                 # ppty_name: [denominator, interested_col]
        'dssp_E': [float(mysys[seq].len), 'Structure'],
        'dssp_H': [float(mysys[seq].len), 'Structure'],
        'dssp_G': [float(mysys[seq].len), 'Structure'],
        'dssp_B': [float(mysys[seq].len), 'Structure'],
        'dssp_C': [float(mysys[seq].len), 'Structure'],
        'dssp_T': [float(mysys[seq].len), 'Structure'],
        'upup'  : [float(mysys[seq].hbg), 'num_upup' ],
        'unun'  : [float(mysys[seq].scnpg),'num_unun'],
        'upun'  : [1., 'num_upun'],
        'upvp'  : [float(mysys[seq].hbg), 'num_upvp' ],
        'upvn'  : [float(mysys[seq].hbg), 'num_upvn' ],
        'unvp'  : [float(mysys[seq].scnpg), 'num_unvp' ],
        'unvn'  : [float(mysys[seq].scnpg), 'num_unvn' ],
        'rg_c_alpha': [1., 'rg_c_alpha']
        }
        for cdt in CDTS:
            tablename = ave_kwargs['tablenamepattern'].format(seq=seq, cdt=cdt)
            print tablename
            if tpostproc_group.__contains__(tablename):
                pass
            else:
                # prepare for creating a new table
                denorminator, interested_col = dd[ppty]
                pfpattern = ave_kwargs['pfpattern']

                aves = []
                for num in NUMS:
                    pf = pfpattern.format(**locals())
                    if h5file.root.ogd.__contains__(pf):
                        t = h5file.getNode(h5file.root.ogd, pf)
                        v = t.read(field=interested_col).mean()
                        v_normed = v / denorminator
                        aves.append(
                            (pf, v_normed.mean(), v_normed.std()) # append a tuple
                            )

            t = h5file.createTable(
                tpostproc_group._v_pathname, tablename, tave, title=(
                    'average value of {0} of each replica normded by {1}'.format(ppty, denorminator)))
            t.append(aves)
    h5file.close()

# I tried with append [str, float, float] to an array, then every element in
# the list will be converted to str, so not convenient for following
# analysis. Then, I choose to create a table instead of an array because I do
# need the pf to each row as an identity
if __name__ == "__main__":
    main()

