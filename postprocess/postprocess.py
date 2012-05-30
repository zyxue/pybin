#! /usr/bin/env python

import os

import tables
from configobj import ConfigObj

# local system level
from argparse_action import get_sctn

# local module level
from common import tave, parse_cmd, loop_h5_alx, loop_h5_ave

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
    tpostproc = args.tpostproc                               # type of postprocess. i.e. ave

    tpostproc_kwargs = conf_dict['postprocess'][tpostproc]

    rootUEP = os.path.join('/', ppty)

    # start dealing with the h5 file
    h5file = tables.openFile(h5filename, 'a', rootUEP=rootUEP)

    tpostproc_group_path = os.path.join('/', tpostproc)
    if h5file.__contains__(tpostproc_group_path): # means first time running tpostproc postprocess for this ppty
        tpostproc_group = h5file.getNode(h5file.root, tpostproc)
    else:
        tpostproc_group = h5file.createGroup(h5file.root, tpostproc)

    if args.tpostproc in ['ave', 'ave10']:
        loop_h5_ave(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, tpostproc_kwargs)
    if args.tpostproc == 'alx':
        loop_h5_alx(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, tpostproc_kwargs)


# I tried with append [str, float, float] to an array, then every element in
# the list will be converted to str, so not convenient for following
# analysis. Then, I choose to create a table instead of an array because I do
# need the pf to each row as an identity
if __name__ == "__main__":
    main()

