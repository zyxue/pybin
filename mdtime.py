#!/usr/bin/env python

import sys
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
        sys.stdout.write(get_cpt_time(args.inputfile))
    elif args.inputfile[-3:] == "tpr":
        sys.stdout.write(get_tpr_time(args.inputfile))
    else:
        sys.stderr.write("Unrecoganized file type\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
