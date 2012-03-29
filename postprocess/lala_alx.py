#! /usr/bin/env python

import os
import argparse

import tables
import numpy as np
from configobj import ConfigObj

from common_func import get_sctn
from mysys import read_mysys

from common import tave, parse_cmd

# def main():
#     args = parse_cmd()

#     # initialization YOU DIAN LUANG!

#     conf = args.conf
#     if not os.path.exists(conf):
#         raise IOError("{0} cannot found".format(conf))

#     conf_dict = ConfigObj(conf)
#     SEQS, CDTS, TMPS, NUMS = get_sctn(args, conf_dict['systems'])

#     h5filename = conf_dict['data']['h5filename']
#     if not os.path.exists(h5filename):
#         raise IOError("{0} cannot found".format(h5filename))

#     ppty = args.ppty
#     tpostproc='alx'                               # type of postprocess. i.e. ave

#     alx_kwargs = conf_dict['postprocess'][tpostproc]

#     rootUEP = os.path.join('/', args.ppty)

#     # start dealing with the h5 file
#     h5file = tables.openFile(h5filename, 'a', rootUEP=rootUEP)

#     tpostproc_group_path = os.path.join('/', tpostproc)
#     if h5file.__contains__(tpostproc_group_path):
#         tpostproc_group = h5file.getNode(h5file.root, tpostproc)
#     else:
#         tpostproc_group = h5file.createGroup(h5file.root, tpostproc)

#     loop_h5_alx(SEQS, CDTS, TMPS, NUMS, h5file, ppty, tpostproc_group, alx_kwargs)


if __name__ == "__main__":
    main()

