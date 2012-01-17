#! /usr/bin/env python

import tables
import argparse

def parse_cmd():
    parser = argparse.ArgumentParser(
        description='print the groups in h5 file recursively, but maxdepth could be specified')
    parser.add_argument('-f', type=str, dest='infile',
                        help='the h5 file')
    parser.add_argument('-n', type=int, dest='maxdepth', default=2,
                        help='you could specify the maxdepth')
    args = parser.parse_args()
    return args

def main():
    args = parse_cmd()
    infile = args.infile
    maxdepth = args.maxdepth
    inf = tables.openFile(infile, 'r')
    nodes_1l = inf.getNode(inf.root)                        # 1l: first level
    for n1l in nodes_1l:
        print n1l._v_pathname
        nodes_2l = inf.getNode(n1l)
        for n2l  in nodes_2l:
            print n2l._v_pathname
    inf.close()

if __name__ == "__main__":
    main()






