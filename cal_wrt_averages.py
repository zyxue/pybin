#!/usr/bin/env python

import re
import glob
import os
import sys
import pprint
import logging
from optparse import OptionParser

import numpy as np
from xvg2png import xvg2array
from Mysys import read_mysys_dat

TYPE_OF_AVERAGES = __all__ = ['cal_wtr_average', 'connect_all_points', 
                              'average_along_x', 'connect_dihedrals']

TYPE_OF_PROPERTIES = ['upvp', 'upvn', 'unvp', 'unvn', 'upup', 'upun', 'unun',
                      'rg', 'upv', 'unv', 'e2ed']

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
    logging.info("%s is done" % outputfile)

def average_along_x(infiles, outputfile, norm):
    """last edited on 2011-11-07"""
    with open(outputfile, 'w') as opf:

        mx, my = {}, {}                                     # map x, map y
        for inf in infiles:
            mx[inf], my[inf] = xvg2array(inf)
            my[inf] /= float(norm)

        ref_inf = infiles[0]
        ref_x, ref_y = mx[ref_inf], my[ref_inf]

        for myk in my.keys():             # check the length of different files
            if len(my[myk]) != len(ref_y):
                raise ValueError("{0} & \n {1} \nhave different number of data points".format(ref_inf, myk))
            # mx won't be checked before it must pass if my passes

        _2d_y = np.array([my[k] for k in my.keys()])
        s = _2d_y.shape
        logging.info(s)                                 # (num_of_file, num_of_data_points)
        l = s[1]
        
        ave_y = [ _2d_y[:,i].mean() for i in range(l)]
        std_y = [ _2d_y[:,i].std() for i in range(l)]
            
        for x,y,s in zip(ref_x, ave_y, std_y):
            opf.write('%10.5f%10.5f%10.5f\n' % (x, y, s))
    logging.info("%s is done" % outputfile)
    return ref_x, ave_y, std_y

def connect_all_points(infiles, outputfile, norm):
    """connecting all points, but the time dependence will be ignored"""
    with open(outputfile, 'w') as opf:
        for k, infile in enumerate(infiles):
            _x, _y = xvg2array(infile)
            _y /= norm
            opf.write("# %s\n" % infile)
            opf.write("%s\n" % (" ".join([str(i) for i in _y])))
    logging.info("%s is done" % outputfile)

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

def parse_cmd():
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
    parser.add_option('--template', type='str', dest='tmpl',
                      default="sq[1-9][wmepo]", help="the template name used to verify the name of infiles. default sq[1-9][wmepo]")

    parser.add_option('--aa', type='str', dest='aa', default=None, 
                      help='Type of amino acid needed with connect_dihedrals')
    options, args = parser.parse_args()

    type_of_aves = __all__

    OPTIONS, args = parser.parse_args()
    return OPTIONS

def main():
    """
    this module is used to process the original_data roughly, obtaining the
    average
    """
    options = parse_cmd()

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
    objid_template = re.compile(options.tmpl)
    objids = [objid_template.search(inf).group() for inf in infiles]
    objids_set = set(objids)
    print objids_set
    if len(objids_set) == 1:
        objid = objids[0]
        seq = objid[:3]
        cdt = objid[3]
        logging.info("objid: %s\t seq: %s\t  cdt: %s" % (objid, seq, cdt))
    else:
        raise ValueError('input files might belong to different objs')
        
    type_of_property = options.tp
    norm = determine_norm(type_of_property, objid)
    logging.info('the denominator for normalization is {0:.2f}'.format(norm))

    if options.ta == 'connect_dihedrals':
        connect_dihedrals(infiles, output, aa=options.aa)
    elif options.ta == 'cal_wtr_average':
        cal_wtr_average(infiles, output, norm)
    elif options.ta == 'average_along_x':
        average_along_x(infiles, output, norm)
    elif options.ta == 'connect_all_points':
        connect_all_points(infiles, output, norm)

if __name__ == "__main__":
    """Usage: e.g.

    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    main()
