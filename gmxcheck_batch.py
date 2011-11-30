#! /usr/bin/env python

import os
import StringIO
import subprocess
import glob
import sys
from optparse import OptionParser

def parse_cmd():
    parser = OptionParser()
    parser.add_option('-f', type='str', dest='fs', 
                      help='specify the cpt files')
    parser.add_option('-t', type='str', dest='time', default='-1', 
                      help='specify the supposed time length of the trajectory')
    parser.add_option('--tmpf', action='store_true', 
                      dest='tmp_cpt_check', default=False, 
                      help='signal that argument is a tmp_cpt_checkfile')
    parser.add_option('--v4_5', action='store_true',
                      dest='v4_5', default=False,
                      help='using the 4_5 version instead')
    global options
    options, args = parser.parse_args()

def gmxcheck_batch():
    if options.tmp_cpt_check:
        infs = [ l.strip() for l in open(options.fs, 'r').readlines() ]
    else:
        infs = sorted(glob.glob(options.fs))
    for inf in infs:
        if options.v4_5:
            gmxcheck = 'gmxcheck4.5'
        else:
            gmxcheck = 'gmxcheck'
        p = subprocess.Popen([gmxcheck,'-f', inf], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = p.communicate()
        if p.returncode == 0:
            pass
        else:
            print '!!! %s is corrupted' % inf
        stderrdata = StringIO.StringIO(stderrdata)
        for line in stderrdata:
            if line.startswith('\r'): 
                # e.g. '\rLast frame         -1 time 200000.016\n'
                if options.time == '-1' :
                    # when t is not specified
                    print '%s # %s' % (inf,line.replace('\r','')),
                elif options.time in line:
                    # when t is specified 
                    pass
                elif options.time != '-1' and not options.time in line:
                    print '%s # %s # %s' % (os.path.dirname(inf),
                                            inf, line.replace('\r','')),

if __name__ == '__main__':
    parse_cmd()
    gmxcheck_batch()
