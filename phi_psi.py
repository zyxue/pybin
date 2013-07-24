#!/usr/bin/env python

import sys
from MDAnalysis import Universe

"""This script currently only applies to sr1 sr2 sr3"""

PHI_SEL = '(resname ACE and name C) or (resname GLY or resname VAL or resname PRO and (name N or name CA or name C))'
PSI_SEL = '(resname GLY or resname VAL or resname PRO and (name N or name CA or name C or name NT)) or (resname NH2 and name N)'


def main(struct):
    u = Universe(struct)

    phi = u.selectAtoms(PHI_SEL)
    psi = u.selectAtoms(PSI_SEL)
    
    print u.filename
    print 'phi: {0:8.2f}'.format(phi.dihedral())
    print 'psi: {0:8.2f}'.format(psi.dihedral())
    print 


if __name__ == "__main__":
    infiles = sys.argv[1:]
    for inf in infiles:
        main(inf)
