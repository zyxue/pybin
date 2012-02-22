#! /usr/bin/env python

import tables
import argparse

def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='h5f', required=True,
                                help='specify the h5f file')
    parser.add_argument('-c', dest='conf', required=True,
                        help='specify the configuration file')
    parser.add_argument('-p', dest='ppty', required=True,
                        help='specify the property your are trying to do ave postprocess on (i.e. rg_c_alpha')
    args = parser.parse_args()
    return args

class tave(tables.IsDescription):
    """table ave"""
    pf = tables.StringCol(itemsize=15, pos=0)    # like an unique id
    ave = tables.Float32Col(pos=1)
    std = tables.Float32Col(pos=2)


