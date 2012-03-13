#! /usr/bin/env python

import sys

import tables
import argparse

from argparse_action import convert_seq, convert_num

def parse_cmd(cmd=None):
    """By default, argparse_action will take sys.argv[1:] as cmd"""

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', dest='SEQS', default=None, nargs='+', action=convert_seq,
                        help="specify it this way, i.e. 1 3 4 or 1-9 (don't include 'sq')")
    parser.add_argument('-c', dest='CDTS', default=None, nargs='+',
                        help="specify it this way, i.e. w m o p e ")
    parser.add_argument('-t', dest='TMPS', default=None, nargs='+',
                        help='specify it this way, i.e "300 700", maybe improved later')
    parser.add_argument('-n', dest='NUMS', default=None, nargs='+', action=convert_num,
                        help='specify the replica number, i.e. 1 2 3 or 1-20')


    parser.add_argument('-f', dest='h5f', required=True,
                        help='specify the h5f file')
    parser.add_argument('-g', dest='conf',
                        help='specify the configuration file')
    parser.add_argument('-p', dest='ppty', required=True,   # ppty: property
                        help='specify the property your are trying to do ave postprocess on (i.e. rg_c_alpha')

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


