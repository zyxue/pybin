#! /usr/bin/env python

import os
import sys
import shutil

def rewrite(infile):
    infile_bk = infile+'.bk'
    if not os.path.exists(infile_bk):
        shutil.copy(infile, infile_bk)
    with open(infile_bk, 'r') as inf:
        with open(infile, 'w') as opf:
            for line in inf:
                p1, p2, p3 = line.strip().partition('=')
                f1, f2, f3 = p1.strip(), p2.strip(), p3.strip()
                opf.write('{0:30s}{1:<2s}{2}\n'.format(f1, f2, f3))
    os.remove(infile_bk)

if __name__ == "__main__":
    rewrite(sys.argv[1])
