#!/usr/bin/env python

import glob
from optparse import OptionParser

import numpy as np

from xvg2png import xvg2array

def connect_p1_p2(p1_file, p2_file, outputfile='lala.xvg'):
    p1 = xvg2array(p1_file)
    p2 = xvg2array(p2_file)
    try:
        p1[0] == p2[0]                        # the same time steps & intervals
    except ValueError:
        print "%s & %s may not belong to the same system" % (p1_file, p2_file)
    p_all = np.array(p1[1]) + np.array(p2[1])
    with open(outputfile, 'w') as opf:
        for time, p in zip(p1[0], p_all):
            opf.write('%15.5f\t%10.5f\n' % (time, p))

# def connect_2_properties(p1_files, p2_files, outputfile):
#     try:
#         len(p1_files) == len(p2_files)
#     except ValueError:
#         print 'NO. of p1_files is different from that of p2_files'
#     for k, (p1_file, p2_file) in enumerate(zip(p1_files, p2_files)):
#         print p1_file, p2_file
#         up_meo = add_p1_p2(p1_file, p2_file)
#         for i in up_meo
#         opf.write('# %s & %s' % (p1_file, p2_file))
#         opf.write('%10d %10.5f\n' % (k, ave_up_meo))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--f1', dest='infile1', default=None)
    parser.add_option('--f2', dest='infile2', default=None)
    parser.add_option('-o', '--outputfile', dest='opf', default=None)
    options, args = parser.parse_args()
    infile1 = options.infile1
    infile2 = options.infile2
    connect_p1_p2(infile1, infile2, options.opf)
