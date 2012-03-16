#! /usr/bin/env python

import sys

import tables
import argparse

from argparse_action import my_basic_parser, convert_seq, convert_num


def parse_cmd(cmd=None):
    parser = my_basic_parser()
    parser.add_argument('-p', '--property-name', type=str, dest='ppty', required=True,
                        help='you must specify the --property-name option from {0!r}'.format(TABLES))
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
