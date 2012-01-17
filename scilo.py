#!/usr/bin/env python

"""
This script is used to wrap the process of file transfer between remote clusters (i.e. SciNet, Collose, Mp2) and my local system.

CAVEAT: options must come at the end of the cmd
"""

import sys
import glob
import subprocess
import argparse

def parse_cmd():
    parser = argparse.ArgumentParser('-f some/file/path -t /SOME/FILE/PATH')
    parser.add_argument('-r', '--recursive', action='store_true', 
                        default=None, dest='recursive', 
                        help='recursive or not')
    parser.add_argument('--l2h', action='store_true', 
                        default=None, dest='l2s', 
                        help='"local to host is specified')
    parser.add_argument('-f', '--from', type=str, dest='from_', required=True,
                        help='From what file')
    parser.add_argument('-t', '--to', type=str, dest='to_', required=True,
                        help='To what file')
    parser.add_argument('--host', type=str, dest='host', default='scinet', 
                        help='specify the host name: s(scinet, default), c(colosse), m(mp2)')
    
    args = parser.parse_args()
    return args

def main():
    DD = {
        's': 'zyxue@login.scinet.utoronto.ca:',
        'c': 'zhuyxue12@colosse.clumeq.ca:',
        'm': 'xuezhuyi@pomes-mp2.ccs.usherbrooke.ca:'
        }

    ARGS = parse_cmd()
    host = DD[ARGS.host]

    if ARGS.l2s:                                         # local to scinet
        local_files = glob.glob(ARGS.from_)
        cmd = (['rsync'] + local_files + 
               [host + ARGS.to_, '--stats', '-h', '-t', '--progress'])
    else:
        cmd = ['rsync', host + ARGS.from_,
               '--stats', '-h', '-t', '--progress']
        if ARGS.to_:
            cmd.insert(2, ARGS.to_)
    if ARGS.recursive:
        cmd.append('-r')
    subprocess.call(cmd)

if __name__ == '__main__':
    main()
