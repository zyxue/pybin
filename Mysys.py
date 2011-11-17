#!/usr/bin/env python

import os
import shutil

class Peptide(object):
    def __init__(self, psp): # psp: Peptide_Specific_Properties
        self.id = psp[0]
        self.seq = psp[1]
        self.col = psp[2]
        self.char = psp[3]
        self.hbg = int(psp[4])
        self.scnpg = int(psp[5])
        self.gptg= float(psp[6])
        self.len= int(psp[7])
        self.tex_seq = psp[8]
        self.order = int(psp[9])
        self.natom = int(psp[10])
        self.seqitp = psp[11]

class Solvent(object):
    def __init__(self, ssp):                  # ssp: Solvent_Specific_Properties
        self.cdt = ssp[0]
        self.name = ssp[1]
        self.col = ssp[2]
        self.solgro = ssp[3]
        self.solitp = ssp[4]
        self.maxsol = ssp[5]
        self.box = ssp[6]
        self.solname =ssp[7]

def read_mysys_dat():
    mysys = {}
    pwd = '/project/pomes/zyxue/pyfiles_scinet'
    with open(os.path.join(pwd, 'mysys.dat'), 'r') as inf:
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
    source = os.path.join(pwd, 'mysys.dat')
    target = os.path.join(pwd, 'mysys.dat.bk')
    shutil.copy(source, target)
    return mysys

if __name__ == "__main__":
    import pprint
    a = read_mysys_dat()
    pprint.pprint(a)
    for k in a.keys():
        print dir(a[k])
