#!/usr/bin/env python

"""
This script is used to wrap the process of file transfer between SciNet,
Collose and my local system.

CAVEAT: options must come at the end of the cmd
"""

import sys
import glob
import subprocess
import optparse

parser = optparse.OptionParser()
parser.add_option('-r', '--recursive', action='store_true', default=None,
                  dest='recursive', help='recursive or not')
parser.add_option('--l2h', action='store_true', default=None,
                  dest='l2s', help='"local to host is specified')
parser.add_option('-f', '--from', type='str', dest='from_', default=None)
parser.add_option('-t', '--to', type='str', dest='to_', default=None)
parser.add_option('--host', type='str', dest='host', default='scinet', help='scinet(default), colosse')


if __name__ == '__main__':
    options, args = parser.parse_args(sys.argv[1:])
    if options.host == 'scinet':
        host = 'zyxue@login.scinet.utoronto.ca:'
    elif options.host == 'colosse':
        host = 'zhuyxue12@colosse.clumeq.ca:'

    if options.l2s:                                         # local to scinet
        local_files = glob.glob(options.from_)
        cmd = ['rsync'] + local_files + [host + options.to_,
            '--stats', '-h', '-t', '--progress']
    else:
        cmd = ['rsync', host + options.from_,
               '--stats', '-h', '-t', '--progress']
        if options.to_:
            cmd.insert(2, options.to_)
    if options.recursive:
        cmd.append('-r')
    subprocess.call(cmd)
