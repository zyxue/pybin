#!/usr/bin/env python

import re
import glob
import os
import sys
import pprint
from optparse import OptionParser

import numpy as np
from xvg2png import xvg2array
from Mysys import read_mysys_dat


mysys = read_mysys_dat()
__all__ = ['cal_wtr_average', 'connect_all_points', 'average_along_x', 'connect_dihedrals']

def cal_wtr_average(infiles, outputfile, norm):                         # norm is the value as the denominator
    with open(outputfile, 'w') as opf:
        aves = []
        for k, infile in enumerate(infiles):
            _x, _y = xvg2array(infile)
            _y /= norm
            ave_y = np.average(_y)
            opf.write('# %s\n' % infile)
            opf.write('%10.2f %10.5f\n' % (k, ave_y))
            aves.append(ave_y)
    return "%s is done" % outputfile

def connect_all_points(infiles, outputfile, norm):
    """connecting all points, but the time dependence will be ignored"""
    with open(outputfile, 'w') as opf:
        for k, infile in enumerate(infiles):
            _x, _y = xvg2array(infile)
            _y /= norm
            opf.write("# %s\n" % infile)
            opf.write("%s\n" % (" ".join([str(i) for i in _y])))
    return "%s is done" % outputfile


def average_along_x(infiles,outputfile,norm):
    with open(outputfile, 'w') as opf:
        mx = {}                                                       # map x
        my = {}                                                       # map y
        k0 = infiles[0]
        for inf in infiles:
            mx[inf],my[inf] = xvg2array(inf)
            my[inf] /= float(norm)                     # while would this be a tuple?!
        l = len(mx[k0])
        assert mx.keys() == my.keys(); keys = mx.keys(); keys.remove(k0)
        for k in keys:
            assert len(mx[k]) == len(my[k]), "invalid data, x & y doesn't match: %s" % k
            if len(mx[k]) < l:                     # get the minimus length of x
                l = len(mx[k])
            assert (mx[k0][:l] == mx[k][:l]).all(),"x axes are not the same in %s & %s" % (k0,k)
        ave_x = mx[k0][:l]
        sum_y = []
        std_y = []
        ys = [my[k0][:l]]
        for k in keys:
            ys.append(my[k][:l])                                      # multi-dimensional array, collecting all data
        ys = np.array(ys)
        for i in range(len(ys[0])):
            sum_y.append(ys[:,i].sum())
            std_y.append(ys[:,i].std())
        ave_y = np.array(sum_y) / float(len(infiles))
        std_y = np.array(std_y)
        assert len(ave_x) == len(ave_y) == len(std_y)
        for x,y,s in zip(ave_x, ave_y, std_y):
            opf.write('%10.5f%10.5f%10.5f\n' % (x,y,s))
    print "%s is done" % outputfile
    return ave_x, ave_y, std_y

def connect_dihedrals(infiles, outputfile='output.xvg', norm=1, aa=None):
    """aa could only be 1 amino acid"""
    if aa:
        template = re.compile('{0}(?!^[@#])'.format(aa)) 
    else:
        template = re.compile('^(\-?\d')

    with open(outputfile, 'w') as opf:
        for infile in infiles:
            opf.write('# %s\n' % infile)
            with open(infile, 'r') as inf:
                for line in inf:
                    if template.search(line):
                        opf.write(line)
    print "%s is done" % outputfile

def determine_norm(type_of_property):
    tp = type_of_property
    if tp in ['unvp','unvn']:
        norm = mysys[seq].scnpg
    elif tp in ['upvp','upvn']:
        norm = mysys[seq].hbg
    elif tp in ['upup']:
        norm = mysys[seq].hbg / 2.
    elif tp in ['upun']:
        norm = mysys[seq].scnpg * mysys[seq].hbg
    elif tp in ['unun']:
        n = mysys[seq].scnpg
        norm = n**2 - n
    elif tp in ["turns","pp2"]:
        norm = mysys[seq].len
    else:
        norm = 1
    return float(norm)

def outline():
    """
    this module is used to process the original_data roughly, obtaining the
    average
    """
    parser = OptionParser()
    parser.add_option('-f', '--infile', type='str', dest='infs', 
                      help='You must specifly at least one file')
    parser.add_option('-p', '--type-of-property', type='str', dest='property', 
                      help='specify the type of property you are dealing with')
    parser.add_option('-t', '--type-of-average', type='str', dest='type_of_ave',
                      help='which kind of average do you want: \n %r' % __all__)
    parser.add_option('-o', '--output_file', type='str', dest='opf',
                      default="output.xvg")
    parser.add_option('--aa', type='str', dest='aa', default=None)
    options, args = parser.parse_args()

    type_of_aves = __all__

    options, args = parser.parse_args()
    infiles = sorted(glob.glob(options.infs))

    if len(infiles) <= 1:
        raise ValueError('the number of input files should be more than 1')
    pprint.pprint(infiles)

    if options.type_of_ave is None:
        raise ValueError('You must specify the value for -t option')
    elif not options.type_of_ave in type_of_aves:
        raise ValueError('k must be in %r' % type_of_aves)

    if options.opf is None:
        ans = raw_input("Are you sure with no specified output name? [y/n]")
        if ans == 'y':
            pass
        else:
            output = raw_input("Then type the the file name:\n")
    else:
        output = options.opf

    id_template = re.compile('sq[1-6][wm]')
    id_s = [id_template.search(inf).group() for inf in infiles]
    if len(set(id_s)) == 1:
        id_ = id_s[0]
        seq = id_[:3]
        cdt = id_[3]
        print id_, seq, cdt
    else:
        raise ValueError('input files have different id_')
        
    tp = options.property
    norm = determine_norm(tp)
    print type(norm)
    print 'the denominator for normalization is {0:.2f}'.format(norm)

    # __all__ = ['cal_wtr_average', 'connect_all_points', 'average_along_x',
    #            'connect_dihedrals']

    if options.type_of_ave == 'connect_dihedrals':
        connect_dihedrals(infiles, output, aa=options.aa)

if __name__ == "__main__":
    """Usage: e.g.

    """
    outline()
