#!/usr/bin/env python
import os
import shutil
from mysys import *

def read():
    mysys = {}
    home = os.getenv('HOME', None)
    with open(os.path.join(home, 'pybin', 'mysys', 'mysys.dat'), 'r') as inf:
        for line in inf:
            if line.strip():
                if line.startswith('@'):
                    sl = line.split()
                    mysys[sl[1]] = Peptide(sl[1:])
                elif line.startswith('&'):
                    sl = line.split()
                    mysys[sl[1]] = Solvent(sl[1:])
                else:
                    pass
    return mysys

if __name__ == "__main__":
    import pprint
    a = read()
    pprint.pprint(a)
    for k in a.keys():
        print dir(a[k])
