#!/usr/bin/env python
import subprocess

class Peptide(object):
    def __init__(self, peptide_specific_properties):
        (self.id,
         self.seq,
         self.col,
         self.char,
         self.up,                                      # polar group of solute
         self.un,                                      # nonpoart group of solute
         self.gptg,
         self.len,
         self.tex_seq,
         self.order,
         self.natom) = peptide_specific_properties

class Solvent(object):
    def __init__(self, solvent_specific_properties):
        (self.cdt,
         self.name,
         self.col) = solvent_specific_properties

class System(object): 
    def __init__(self, system_specific_properties):
        (self.tid, 
         self.nm_unvn,
         self.nm_unvp,
         self.nm_upvn,
         self.nm_upvp,
         self.nm_unun,
         self.nm_unup,
         self.nm_upup,
         self.nm_upv,
         self.nm_unv) = system_specific_properties

def read_mysys_dat():
    mysys = {}
    with open('/home/zyxue/pyfiles_desktop/mysys.dat') as inf:
        for line in inf:
            if line.strip():
                sl = line.split()
                if line.startswith('@'):
                    mysys[sl[1]] = Peptide(sl[1:])
                elif line.startswith('&'):
                    mysys[sl[1]] = Solvent(sl[1:])
                elif line.startswith('$'):
                    mysys[sl[1]] = System(sl[1:])
                else:
                    pass
    subprocess.call('cp ~/pyfiles_desktop/mysys.dat ~/pyfiles_desktop/mysys.dat.bk',shell=True)
    return mysys

if __name__ == "__main__":
    import pprint
    a = read_mysys_dat()
    pprint.pprint(a)
    for k in a.keys():
        print dir(a[k])
