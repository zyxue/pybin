#! /usr/bin/env python

import os
import numpy as np
import shutil

import argparse

def get_len(infile):
    with open(infile, 'r') as inf:
        return len(inf.readlines())

def parse_cmd():
    parser = argparse.ArgumentParser(
        description='to unify rdf radius so that alx could work')
    parser.add_argument('-t', type=str, dest='trdf', 
                        help='type of rdf, i.e. rdf_upup, rdf_unvn')
    args = parser.parse_args()
    return args

def main():
    """rough code: you need to change rdf_unvn, and modify the path everytime"""
    args = parse_cmd()
    trdf = args.trdf
    SEQS = os.getenv('SEQS').split()
    CDTS = os.getenv('CDTS').split()
    if trdf.endswith('vn'):
        CDTS.remove('w')
    NUMS = os.getenv('NUMS').split()

    for s in SEQS:
        for c in CDTS:
            infiles = [os.path.join(
                    'r_{trdf}'.format(trdf=trdf),
                    '{s}{c}300s{n}_{trdf}.xvg'.format(**locals())
                    ) for n in NUMS]
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

if __name__ == "__main__":
    main()
        
