#!/usr/bin/env python

import argparse
from common_func import get_cpt_time


def parse_cmd():
    parser = argparse.ArgumentParser(
        prog='specify the gmxcheck version, and cpt file as input')
    parser.add_argument('-f', type=str, dest='inputfile', required=True,
                        help='specify the inputfile')
    parser.add_argument('--vv', type=str, dest='cptversion', default='4_0',
                        help='speicify the gromacs version, e.g. 4_0 or 4_5')
    args = parser.parse_args()
    return args

def main():
    args = parse_cmd()
    cpttime = get_cpt_time(args.inputfile)
    print cpttime

if __name__ == "__main__":
    main()
    
    
