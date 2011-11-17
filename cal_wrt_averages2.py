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

"""This script is trying to prove the guess:
Only_meo:
    upup > upun                                # normalized by the number of up
    unun > upun                                # normalized by the number of un

    upvp > upvn                                # normalized by the number of up
    unvn > unvp                                # normalized by the number of un
"""

TYPE_OF_AVERAGES = __all__ = ['cal_wtr_average']

TYPE_OF_PROPERTIES = ['upup', 'upun', 'unun', 'upvp', 'upvn', 'unvn', 'unvp']

def cal_wtr_average(infiles, outputfile, norm):
    with open(outputfile, 'w') as opf:
        for k, infile in enumerate(infiles):
            x, y = xvg2array(infile)
            y /= norm
            ave_y = np.average(y)
            opf.write('# %s\n' % infile)
            opf.write('%10d %10.5f\n' % (k, ave_y))
    return "%s is done" % outputfile

def determine_norm(type_of_property, obj):
    """
    This function needs to be modified if you need specific normalization other
    than 1
    """
    mysys = read_mysys_dat()
    tp = type_of_property
    if tp == 'unvn':
        norm = mysys[obj].nm_unvn
    elif tp == 'unvp':
        norm = mysys[obj].nm_unvp
    elif tp == 'upvn':
        norm = mysys[obj].nm_upvn
    elif tp == 'upvp':
        norm = mysys[obj].nm_upvp
    elif tp == 'unun':
        norm = mysys[obj].nm_unun
    elif tp == 'unvp':
        norm = mysys[obj].nm_unvp
    elif tp == 'upup':
        norm = mysys[obj].nm_upup
    elif tp == 'upv':
        norm = mysys[obj].nm_upv
    elif tp == 'unv':
        norm = mysys[obj].nm_unv
    elif tp in ['turns', 'pp2']:
        norm = mysys[obj[:3]].len
    else:
        norm = 1
    return float(norm)

def outline():
    """
    this module is used to process the original_data roughly, obtaining the
    average
    """
    parser = OptionParser()
    parser.add_option('-f', '--infiles', type='str', dest='infiles', 
                      default=None, help='You must specifly at least one file')
    parser.add_option('-p', '--type-of-property', type='str', dest='tp', 
                      help='Specify the type of property dealt with:\n%r' %
                      TYPE_OF_PROPERTIES)
    parser.add_option('-t', '--type-of-average', type='str', dest='ta',
                      help='Specify the type of average calculated:\n%r' % 
                      TYPE_OF_AVERAGES)
    parser.add_option('-o', '--output_file', type='str', dest='opf',
                      default="output.xvg", help="the name of output file")
    parser.add_option('--aa', type='str', dest='aa', default=None, 
                      help='Type of amino acid needed with connect_dihedrals')
    options, args = parser.parse_args()

    type_of_aves = __all__

    options, args = parser.parse_args()

    # Verify the options specified
    if not options.infiles:
        raise ValueError("You must specify -f") 

    if not options.tp in TYPE_OF_PROPERTIES:
        raise ValueError(
            """You must specify the value for -p --type-of-property option,
            and its value must be one of \n %r""" % TYPE_OF_PROPERTIES)

    if not options.ta in TYPE_OF_AVERAGES:
        raise ValueError(
            """You must specify the value for -t --type-of-average option,
            and its value must be one of \n %r""" % TYPE_OF_AVERAGES)

    if options.opf is None:
        ans = raw_input("Are you sure with no specified output name? [y/n]")
        if ans == 'y':
            pass
        else:
            output = raw_input("Then type the the file name:\n")
    else:
        output = options.opf

    infiles = sorted(glob.glob(options.infiles))
    if len(infiles) < 1:
        raise ValueError('the number of input files should > 1')
    pprint.pprint(infiles)

    # Check if those infiles belong to the same type of system
    objid_template = re.compile('sq[1-6][wm]')
    objids = [objid_template.search(inf).group() for inf in infiles]
    if len(set(objids)) == 1:
        objid = objids[0]
        seq = objid[:3]
        cdt = objid[3]
        print "objid: %s\t seq: %s\t  cdt: %s" % (objid, seq, cdt)
    else:
        raise ValueError('input files might belong to different objs')
        
    type_of_property= options.tp
    norm = determine_norm(type_of_property, objid)
    print 'the denominator for normalization is {0:.2f}'.format(norm)

    if options.ta == 'connect_dihedrals':
        connect_dihedrals(infiles, output, aa=options.aa)
    elif options.ta == 'cal_wtr_average':
        cal_wtr_average(infiles, output, norm)

if __name__ == "__main__":
    """Usage: e.g.

    """
    outline()
