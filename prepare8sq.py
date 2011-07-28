#!/usr/bin/python

import sys

def prepare8sq_top(inf='sq.top',opf1='8sq.top',opf2='sq.itp'):
    infile = open(inf, 'r')
    opfile1 = open(opf1, 'w')
    opfile2 = open(opf2, 'w')
    lines = infile.readlines()
    k = 0                       # a counter
    while not lines[k].startswith('[ moleculetype ]'):
        opfile1.write(lines[k])
        k+=1
    opfile1.write('#include "%s"\n\n' % opf2) # e.g. #include "sq.itp"
    while not lines[k].startswith('; Include Position restraint file'):
        if lines[k].startswith('Protein'):
            opfile2.write(lines[k].replace('Protein',opf2[:-4]))
            k+=1
        else:
            opfile2.write(lines[k])
            k+=1
    while not lines[k].startswith('[ molecules ]'):
        if lines[k].startswith('Protein'):
            opfile1.write(lines[k].replace('Protein',opf1[:-4]))
            k+=1
        else:
            opfile1.write(lines[k])
            k+=1
    len_lines = len(lines)
    while k < len_lines:
        if lines[k].startswith('Protein'):
            opfile1.write(lines[k].replace('Protein',opf2[:-4]).replace(' 1',' 8'))
        else:
            opfile1.write(lines[k])
        k+=1

if __name__ == "__main__":
    """
    sys.argv[1]: sq.top
    sys.argv[2]: 8sq.top
    sys.argv[3]: sq.itp
    """
    prepare8sq_top(sys.argv[1],sys.argv[2],sys.argv[3])
