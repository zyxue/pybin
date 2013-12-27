#!/usr/bin/env python

"""Calculate the backbone dihedral angles of a pdb file"""

import sys
import argparse
import Queue
from threading import Thread

import numpy as np
from MDAnalysis import Universe
from MDAnalysis.core.AtomGroup import AtomGroup

MAP3to1 = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D",
    "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G",
    "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
    "MET": "M", "PHE": "F", "PRO": "P", "SER": "S",
    "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    }

MAP1to3 = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP",
    "C": "CYS", "Q": "GLN", "E": "GLU", "G": "GLY",
    "H": "HIS", "I": "ILE", "L": "LEU", "K": "LYS",
    "M": "MET", "F": "PHE", "P": "PRO", "S": "SER",
    "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL",
    }

def main():
    args = get_args()
    if args.pdbs is not None: 
        flist = args.pdbs     # if pdbs is specified, skip the filelist
    elif args.filelist is not None:
        flist = get_files(args.filelist)
    else:
        raise ValueError("either pdbs or filelist should not be None")

    if args.output:
        opf = open(args.output, 'w', 0) # 0 means unbuffered, so don't need to do flush()
        errf = open('{0}.error'.format(args.output), 'w', 0)
    else:
        opf = sys.stdout
        errf = sys.stderr

    working_q = Queue.Queue(maxsize=200)
    writing_q = Queue.Queue(maxsize=200)
    for i in range(14):
        t = Thread(target=worker, args=[working_q, writing_q])
        t.daemon = True
        t.start()

    wt = Thread(target=writing, args=[writing_q, opf, errf])
    wt.daemon = True
    wt.start()

    for filename in flist:
        working_q.put([filename, opf, errf])
    working_q.join()

def worker(q, wq):
    while True:
        filename, opf, errf = q.get()
        output = process(filename, opf, errf)
        wq.put(output)
        q.task_done()

def writing(q, opf, errf):
    while True:
        stuff = q.get()
        if stuff[0] == 0:
            opf.write(stuff[1])
        else:
            errf.write(stuff[1])

def process(filename, opf, errf):
    """process a single file"""
    try:
        # print filename
        if filename.endswith('.pdb') or filename.endswith('.ent.gz'):
            # .ent.gz can be seen from files downloaded in large amount from pdb website
            univ = Universe(filename, format='pdb')
        elif filename.endswith('.gro'):
            univ = Universe(filename, format='gro')
        else:
            raise ValueError("unrecognized file format: {0}".format(filename))
        tets = select_dihedrals(univ)
        if tets:
            hdrs = [''.join([swap_aa_name(_) for _ in tet.resnames()]) for tet in tets]
            dihs = calc_dihs(tets)
            title = ' '.join('{0:<4s}'.format(h) for h in hdrs)
            content = ' '.join('{0:<4d}'.format(d) for d in dihs)
        else:
            title, content = '', ''

        # print title
        # print content
        return [0, "{0}\n{1}\n{2}\n".format(filename, title, content)]
    except Exception as err:
        return [1, "{0}\n{1}\n{2}\n{0}\n".format('#' * 79, filename, err)]

def get_files(filelist):
    with open(filelist, 'rb') as flist:
        for _ in flist:
            yield _.strip()

def calc_dih(tet):
    dih = np.float64(np.nan_to_num(tet.dihedral()))
    # for some reason numpy.float32, the type of which dihedral
    # angle is returned in cannot be formatted by {0:f} either
    # (python 2.7.2 + numpy 1.6.1) or (python 2.7.2 + numpy 1.6.1)
    # works, use convert to float

    # equivalent to delta = abs(abs(dih) - 180) - abs(dih - 0)
    delta = abs(abs(dih) - 180) - abs(dih)
    # if dih is closer to 180: trans (i.e delta <=0, symbol 0)
    # Otherwis, closer to 0  : cis   (i.e delta > 1, symbol 1)
    dih = 0 if delta <= 0 else 1
    return dih
    
def calc_dihs(tets):
    dihs = []
    for tet in tets:
        dihs.append(calc_dih(tet))
    return dihs


def select_dihedrals(univer):
    CA = univer.selectAtoms('name CA and not resname ACE and not resname NH2')
    C  = univer.selectAtoms('name C  and not resname ACE and not resname NH2')
    N  = univer.selectAtoms('name N  and not resname ACE and not resname NH2')

    ##########ILLUSTRATION: 2 DIHEDRAL ANGLE FORMD BY 3 RESIDUES############
    # dihedral: // or \\
    #             O
    #             "
    #   Ca   N    C    Ca   O-H
    #  /  \ //\  / \\ /  \ /
    # N    C   Ca    N    C
    #      "              "
    #      O              O

    tets = []
    if CA and C and N:
        for ca1, c, n, ca2 in zip(CA[:-1], C[:-1], N[1:], CA[1:]):
            # ignore resiudes other than the 20
            if (ca1.resname in MAP3to1.keys() and
                  c.resname in MAP3to1.keys() and
                  n.resname in MAP3to1.keys() and
                ca2.resname in MAP3to1.keys()):
                # only interested in X-Pro, filter out all others
                if n.resname == 'PRO' and ca2.resname == 'PRO':
                    if right_atom_order(ca1, c, n, ca2):
                        tet = [ca1, c, n, ca2]
                        tets.append(AtomGroup(tet))
    return tets

def right_atom_order(ca1, c, n, ca2):
    # there can be cases caused by conflicts from different db, identified by
    # SEQADV record, ignore those for now.
    return (ca1.resid == c.resid and
            n.resid == ca2.resid and 
            ca2.resid - ca1.resid == 1)

def swap_aa_name(abbr):
    if len(abbr) == 3:
        return MAP3to1[abbr]
    elif len(abbr) == 1:
        return MAP1to3[abbr]

def get_args(args=None):
    p = argparse.ArgumentParser()
    p.add_argument('-f', dest='pdbs', nargs='+', help='specify one or more pdb files')
    p.add_argument('--filelist', dest='filelist', help='you can also specify a file containing a list of pdbfiles')
    p.add_argument('-o', dest='output', nargs='+', help='if specified, stdin stdout will be redirected to the output instead of terminal')
    args = p.parse_args()
    return args

if __name__ == "__main__":
    main()
