#!/usr/bin/env python
import os
import shutil
import mysys

def read():
    data_of_mysys = {}
    # mysys_pwd: the directory where mysys is located
    mysys_pwd = os.path.dirname(__file__) 

    with open(os.path.join(mysys_pwd, 'mysys.dat'), 'r') as inf:
        for line in inf:
            if line.strip():
                if line.startswith('@'):
                    sl = line.split()
                    data_of_mysys[sl[1]] = mysys.Peptide(sl[1:])
                elif line.startswith('&'):
                    sl = line.split()
                    data_of_mysys[sl[1]] = mysys.Solvent(sl[1:])
                elif line.startswith('$'): 
                    sl = line.split()
                    data_of_mysys[sl[1]] = mysys.Mono_sys(sl[1:])
                else:
                    pass
    return data_of_mysys

if __name__ == "__main__":
    import pprint
    a = read()
    print a['sq1w'].nm_unv
#     for k in a.keys():
#         print dir(a[k])
