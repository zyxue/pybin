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
    if args.cptversion == '4_5':
        cpttime = get_cpt_time(
            args.inputfile,
            '/home/p/pomes/zyxue/exec/gromacs-4.5.5/exec/bin/gmxcheck')
    elif args.cptversion == '4_0':
        cpttime = get_cpt_time(
            args.inputfile,
            '/home/p/pomes/zyxue/exec/gromacs-4.0.5/exec/bin/gmxcheck')
    else:
        raise ValueError("version unrecoganized!")
    print cpttime

if __name__ == "__main__":
    main()
    
    
