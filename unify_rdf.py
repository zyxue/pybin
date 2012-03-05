#! /usr/bin/env python

import os
import numpy as np
import shutil
import glob

import argparse

def get_len(infile):
    with open(infile, 'r') as inf:
        return len(inf.readlines())

def parse_cmd():
    parser = argparse.ArgumentParser(
        description='to unify rdf radius so that alx could work')
    parser.add_argument('-f', type=str, dest="infiles", required=True, nargs='+',
                        help="files contain rdf data that are to be unified")
    parser.add_argument('--delbk', dest='delbk', action='store_true', default=False,
                        help='del the bk file or not')
    args = parser.parse_args()
    return args

def main():
    """rough code: you need to change rdf_unvn, and modify the path everytime"""
    args = parse_cmd()
    infiles = args.infiles

    min_len = np.min([get_len(f) for f in infiles])
    for f in infiles:
        print f
        f_bk = f + '.bk'
        os.rename(f, f_bk)
        bk_f = open(f_bk, 'r')
        bk_lines = bk_f.readlines()[:min_len]
        bk_f.close()
        with open(f, 'w') as ftw:                   # file to write
            ftw.writelines(bk_lines)
        if args.delbk:
            os.remove(f_bk)

if __name__ == "__main__":
    main()
        
