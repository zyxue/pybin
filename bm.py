#!/usr/bin/python

import sys
def bm(n):
    """ You need to prepare the bm1.sh file which use just 1 node"""
    for num in range(2,n+1):
        infile = open('bm01.sh', 'r')
        opfile = open('bm%02d.sh' % num, 'w')
        for line in infile:
            if line.startswith('#PBS -l'):
                opfile.write(
                    '#PBS -l nodes=%d:ib:ppn=8,walltime=00:06:00,os=centos53computeA\n' % num)
            elif line.startswith('#PBS -N'):
                opfile.write('#PBS -N bm%02dn\n' % num)
            else:
                opfile.write(line)
        infile.close()

if __name__ == '__main__':
    bm(int(sys.argv[1]))
