#! /usr/bin/env python

import os
import subprocess
import StringIO
import argparse
import time
import re

__version__ = 2

class showq(object):
    def __init__(self):
        pipe = subprocess.PIPE
        p = subprocess.Popen(['showq', '--noblock'], stdout=pipe, stderr=pipe)
        stdoutdata, stderrdata = p.communicate()
        self.stdout = stdoutdata
        self.stderr = stderrdata
        self.returncode = p.returncode

def collect_data(accounts, data_list, host, fgg, fib):
    cores_usage = {}
    for ll in data_list:
        sl = ll.split()
        if len(sl) == 9:
            user = sl[1]
            if user in accounts:
                if host == 'm':
                    # on mp2, showq display the number of nodes in PROC column
                    ncore = int(sl[3]) * 24 
                    n = ncore                               # to be consistent with the scinet condition
                elif host == 's':
                    # on scinet, showq display the number of cores in PROC column
                    ncore = int(sl[3])
                    check1 = (not fib) and (not fgg)
                    check2 = fgg and ncore == 8
                    check3 = fib and ncore > 8
                    if check1 or check2 or check3:
                        n = ncore
                    else:
                        n = 0                               # forgot what wierd would fit this condition
                elif host == 'l':
                    # on lattice, showq display the number of cores in PROC column
                    ncore = int(sl[3])
                    n = ncore
                if user in cores_usage:
                    cores_usage[user] += n
                else:
                    cores_usage[user] = n

    return cores_usage

def parse_cmd():
    parser = argparse.ArgumentParser(prog='you need to specify the host')
    parser.add_argument('--host', type=str, dest='host', default='s',
                        help='specify the host name: s(scinet, default), c(colosse), m(mp2), l(lattice)')
    parser.add_argument('-n', '--by-node', action='store_true', dest='bn', default=False,
                      help='show the number of nodes instead of cores')
    
    # scient argument group
    gscinet = parser.add_argument_group(title='SciNet', 
                                        description='options in this group only works on SciNet')
    gscinet.add_argument('--gg', action='store_true', dest='fgg', default=False,
                       help='show the number of GigE cores only')
    gscinet.add_argument('--ib', action='store_true', dest='fib', default=False,
                       help='show the number of ib cores only')
    gscinet.add_argument('--machine', action='store_true', dest='fmachine', default=False,
                       help='generate data easy for machine process')

    args = parser.parse_args()
    return args

def print_usage(accounts, acu, bcu, ccu, fmachine):
    total_usage = {}
    for a in accounts:
        total_usage[a] = acu.get(a, 0) + bcu.get(a, 0) + ccu.get(a, 0)

    if fmachine:
        print '{0}, {1}, {2}'.format(sum(acu.values()), time.time(), time.ctime())
    else:
        print "{0:10s} {1:8s} {2:8s} {3:8s} {4:8s}\n{5:44s}".format(
            'USERNAME', 'ACTIVE', 'ELIGIBLE', 'BLOCKED', 'TOTAL', "=" * 44)
        sorted_keys = reversed(sorted(total_usage, key=total_usage.get))
        for k in sorted_keys:
            print "{0:10s} {1:<8d} {2:<8d} {3:<8d} {4:<8d}".format(
                k, acu.get(k, 0), bcu.get(k, 0), ccu.get(k, 0), total_usage[k])

def main():
    args = parse_cmd()

    if args.host == 'm':
        accounts = os.listdir('/mnt/scratch_mp2/pomes/')
        accounts.remove('pomes_group')
    elif args.host == 's':
        accounts = os.listdir('/scratch/p/pomes/')
    elif args.host == 'l':
        accounts = ['zyxue', 'grace']

    r_showq = showq()                                       # r_showq: result of showq
    if r_showq.returncode != 0 or r_showq.stderr != '':
        raise IOError('Check the returncode: {0:d}\n and stderrdata: {1!s}\n'.format(
                r_showq.returncode, r_showq.stderr))

    output = StringIO.StringIO(r_showq.stdout)
    # 
    # How try to divide the output into three sections
    section_headers = ['active jobs', 'eligible jobs', 'blocked jobs']
    if args.host == 'm':
        section_headers[1] = 'idle jobs'

    ll = output.readline()
    while not ll.lower().startswith(section_headers[0]):
        ll = output.readline()

    alist = []                                              # active_cores_usage
    while not ll.lower().startswith(section_headers[1]):
        if re.search('processor', ll, re.IGNORECASE):
            print ll

        alist.append(ll)
        ll = output.readline()

    blist = []                                             # eligible/idle_cores_usage
    while not ll.lower().startswith(section_headers[2]):
        blist.append(ll)
        ll = output.readline()
        
    clist = []                                               # blocked_cores_usage
    while ll:
        clist.append(ll)
        ll = output.readline()

    acu = collect_data(accounts, alist, args.host, args.fib, args.fgg)
    bcu = collect_data(accounts, blist, args.host, args.fib, args.fgg)
    ccu = collect_data(accounts, clist, args.host, args.fib, args.fgg)

    print_usage(accounts, acu, bcu, ccu, args.fmachine)

if __name__ == "__main__":
    main()
