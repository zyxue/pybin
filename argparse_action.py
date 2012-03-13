#! /usr/bin/env python

"""This script contains class that are expected to be commonly used for my other scripts"""

import argparse


class convert_seq(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        processed_values = []
        for v in values:
            if '-' in v:
                mi, ma = (int(i) for i in values[0].split('-'))
                v = [str(i) for i in xrange(mi, ma + 1)]
                processed_values.extend(v)
            else:
                processed_values.append(v)

        final_values = ['sq{0}'.format(i) for i in processed_values]
        setattr(namespace, self.dest, final_values)

class convert_num(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        processed_values = []
        for v in values:
            if '-' in v:
                mi, ma = (int(i) for i in values[0].split('-'))
                v = [i for i in xrange(mi, ma + 1)]
                processed_values.extend(v)
            else:
                processed_values.append(int(v))

        final_values = ['{0:02d}'.format(v) for v in processed_values]
        setattr(namespace, self.dest, final_values)

# If the above works, delete the following two classes

# class convert_seq(argparse.Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         if len(values) > 1:
#             v = values
#         else:
#             vv = values[0]
#             if '-' in vv:
#                 mi, ma = (int(i) for i in values[0].split('-'))
#                 v = [str(i) for i in xrange(mi, ma + 1)]
#             else:
#                 v = values
#         setattr(namespace, self.dest, ['sq{0}'.format(i) for i in v])

# class convert_num(argparse.Action):
#     def __call__(self, parser, namespace, values, option_string=None):
#         if len(values) > 1:
#             v = ['{0:02d}'.format(i) for i in (int(j) for j in values)]
#         else:
#             vv = values[0]
#             if '-' in vv:
#                 mi, ma = (int(i) for i in vv.split('-'))
#                 v = ['{0:02d}'.format(i) for i in xrange(mi, ma + 1)]
#             else:
#                 v = ['{0:02d}'.format(int(values[0]))]
#         setattr(namespace, self.dest, v)


# class Myparser(argparse.ArgumentParser):
#     def __init__(self):
#         self.add_argument('-s', dest='SEQS', nargs='+', action=convert_seq,
#                             help="specify it this way, i.e. 1 3 4 or 1-9 (don't include 'sq')")
#         self.add_argument('-c', dest='CDTS', nargs='+',
#                             help="specify it this way, i.e. w m o p e ")
#         self.add_argument('-t', dest='TMPS', default=None, nargs='+',
#                             help='specify it this way, i.e "300 700", maybe improved later')
#         self.add_argument('-n', dest='NUMS', nargs='+', action=convert_num, required=True,
#                             help='specify the replica number, i.e. 1 2 3 or 1-20')
def myparser():
    """parse_cmd"""
    parser = argparse.ArgumentParser(usage="-s, -c, -t, -n (don't use quotes)")

    parser.add_argument('-s', dest='SEQS', nargs='+', action=convert_seq,
                        help="specify it this way, i.e. 1 3 4 or 1-9 (don't include 'sq')")
    parser.add_argument('-c', dest='CDTS', nargs='+',
                        help="specify it this way, i.e. w m o p e ")
    parser.add_argument('-t', dest='TMPS', default=None, nargs='+',
                        help='specify it this way, i.e "300 700", maybe improved later')
    parser.add_argument('-n', dest='NUMS', nargs='+', action=convert_num, required=True,
                        help='specify the replica number, i.e. 1 2 3 or 1-20')
    return parser
