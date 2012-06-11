#! /usr/bin/env python

"""This script contains class that are expected to be commonly used for my other scripts"""

import re
import argparse

class convert_seq(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        processed_values = []
        for v in values:
            # match = re.search("([a-z]+)\[?([0-9]+-?[0-9]*)\]?", v)
            # bash will separate [1-4] autmatically, so commented out the above line
            match = re.search("([a-z]+)([0-9]+-?[0-9]*)", v)
            # print match.groups()
            pf, index = match.groups()
            if '-' in index:
                mi, ma = (int(i) for i in index.split('-'))
                v = [pf+str(i) for i in xrange(mi, ma + 1)]
                processed_values.extend(v)
            else:
                processed_values.append(v)

            # final_values = ['{0}{1}'.format(pf,i) for i in processed_values]
            final_values = processed_values
        setattr(namespace, self.dest, final_values)

class convert_num(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        processed_values = []
        for v in values:
            if '-' in v:
                mi, ma = (int(i) for i in v.split('-'))
                v = [i for i in xrange(mi, ma + 1)]
                processed_values.extend(v)
            else:
                processed_values.append(int(v))
        final_values = ['{0:02d}'.format(v) for v in processed_values]
        setattr(namespace, self.dest, final_values)

def my_basic_parser():
    """By default, argparse_action will take sys.argv[1:] as cmd"""

    my_basic_parser = argparse.ArgumentParser()

    my_basic_parser.add_argument('-s', dest='SEQS', default=None, nargs='+', action=convert_seq,
                        help="specify it this way, i.e. 1 3 4 or 1-9 or 1, 3-5 (don't include 'sq')")
    my_basic_parser.add_argument('-c', dest='CDTS', default=None, nargs='+',
                        help="specify it this way, i.e. w m o p e ")
    my_basic_parser.add_argument('-t', dest='TMPS', default=None, nargs='+',
                        help='specify it this way, i.e "300 700", maybe improved later')
    my_basic_parser.add_argument('-n', dest='NUMS', default=None, nargs='+', action=convert_num,
                        help='specify the replica number, i.e. 1 2 3 or 1-20 or 1, 3, 4-7')
    return my_basic_parser

def get_sctn(args, configuration):
    SEQS = args.SEQS if args.SEQS else configuration['SEQS']
    CDTS = args.CDTS if args.CDTS else configuration['CDTS']
    TMPS = args.TMPS if args.TMPS else configuration['TMPS']
    NUMS = args.NUMS if args.NUMS else configuration['NUMS']
    return SEQS, CDTS, TMPS, NUMS
