#!/usr/bin/env python

"""
This script is used to wrap the process of file transfer between remote
clusters (i.e. SciNet, Collose, Mp2) and my local system.

CAVEAT: options must come at the end of the cmd
"""

import glob
import subprocess
import argparse

def parse_cmd():
    parser = argparse.ArgumentParser('-f some/file/path -t /SOME/FILE/PATH')
    parser.add_argument('-r', '--recursive', action='store_true', 
                        default=None, dest='recursive', 
                        help='recursive or not')
    parser.add_argument('--l2h', action='store_true', 
                        default=None, dest='l2h', 
                        help='"local to host is specified')
    parser.add_argument('-f', '--from', dest='from_', required=True, nargs="+",
                        help='From what file')
    parser.add_argument('-L', dest='L', action='store_true',
                        help='check rsync')
    parser.add_argument('-t', '--to', type=str, dest='to_', required=True,
                        help='To what file')
    parser.add_argument('--host', type=str, dest='host', default='s', 
                        help=('specify the host name: '
                              's(scinet, default), c(colosse), m(mp2)'
                              'g(guillimin), l(lattice), o(orca)'))
    
    args = parser.parse_args()
    return args

def main():
    DD = {
        's': 'zyxue@login.scinet.utoronto.ca:',
        'b': 'zyxue@bgqdev.scinet.utoronto.ca:',
        'c': 'zhuyxue12@colosse.clumeq.ca:',
        'm': 'xuezhuyi@pomes-mp2.ccs.usherbrooke.ca:',
        'n': 'zyxue@nestor.westgrid.ca:',
        'l': 'zyxue@lattice.westgrid.ca:',
        'p': 'zyxue@parallel.westgrid.ca:',
        'g': 'zhuyxue12@guillimin.clumeq.ca:',
        'o': 'zyxue@orca.sharcnet.ca:',
        'i': 'zyxue@orcinus.westgrid.ca:',
        't': 'zyxue@tera.research.sickkids.ca:',
        't2': 'zyxue@t2.research.sickkids.ca:',

        # at bcgsc
        'genesis': 'zxue@genesis.bcgsc.ca:',
        }

    ARGS = parse_cmd()
    host = DD[ARGS.host]

    if ARGS.l2h:                                         # local to scinet
        lfl = []                            # local_files_list
        for i in ARGS.from_:
            lfl.extend(glob.glob(i))
        cmd = (['rsync'] + lfl + 
               [host + ARGS.to_, '--stats', '-h', '-t', '--progress', '-a'])
    else:
        cmd = ['rsync', host + ''.join(ARGS.from_),
               '--stats', '-h', '-t', '--progress']
        if ARGS.to_:
            cmd.insert(2, ARGS.to_)
    if ARGS.recursive:
        cmd.append('-r')
    if ARGS.L:
        cmd.append('-L')

    subprocess.call(cmd)

if __name__ == '__main__':
    main()
