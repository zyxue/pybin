#!/usr/bin/env python

import argparse
from common_func import get_cpt_time, get_tpr_time

def parse_cmd():
    parser = argparse.ArgumentParser(
        prog='specify the gmxcheck version, and cpt file as input')
    parser.add_argument('-f', type=str, dest='inputfile', required=True,
                        help='specify the inputfile')
    args = parser.parse_args()
    return args

def main():
    args = parse_cmd()
    if args.inputfile[-3:] == "cpt":
        t = get_cpt_time(args.inputfile)
    elif args.inputfile[-3:] == "tpr":
        t = get_tpr_time(args.inputfile)
    print t

if __name__ == "__main__":
    main()
    
    
