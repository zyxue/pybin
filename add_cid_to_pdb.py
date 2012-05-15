#! /usr/bin/env python

import sys
import string

def add_cid(atom_line, symbol):
    """
    atom_line should be a list of values for pdb colums
    symbol is the chain distinguishment"
    """
    atom_line.pop(5)                                        # remove the old cid
    atom_line.insert(5, symbol)                             # add the new one

    # This format is nearly right but unfamiliar items lie occu, bfac, segid,
    # elsy, charge haven't been tested

    return "{0:<6s}{1:>5s} {2:>4s}{3:1s}{4:>3s} {5:1s}{6:>4s}{7:1s}   {8:>8s}{9:>8s}{10:>8s}{11:6s}{12:6s}{13:4s}{14:2s}{15:2s}\n".format(*atom_line)

def parse_pdb(infile):
    with open(infile, 'r') as inf:
        for line in inf:
            if line.startswith("ATOM") and 'W' not in line:
                line = line.strip().ljust(80) # incase some cols are empty in terms of pdb format
                recn = line[0:6].strip()              # record name
                aid_ = line[6:12].strip()             # atom id
                name = line[12:16].strip()            # atom name
                char = line[16].strip()               # alternate location indicator: not sure what it is
                resname = line[17:21].strip()         # residue name
                cid  = line[21].strip()               # chain id, if this script is used, probably cid is empty
                resid = line[22:26].strip()           # residue id
                achar = line[26].strip()              # code for insertion of residues, not sure what it is
                x = line[30:38].strip()
                y = line[38:46].strip()
                z = line[46:54].strip()
                occu = line[54:60].strip()            # occupancy
                bfac = line[60:66].strip()            # b factor, or called temperature factor
                segid = line[72:76].strip()           # segment identifier, left, justified
                elsy  = line[76:78].strip()           # element symbol ,right justified
                charge = line[78-80].strip()          # charge on the atom
                yield [recn, aid_, name, char, resname, cid , resid, achar, x, y, z, 
                        occu, bfac, segid, elsy , charge]
            else:
                yield line

def main(infile, outputfile, natom):
    """natom: number of atoms in a monomer"""
    symbols = string.printable
    atom_count = 0
    chain_count = 0
    with open(outputfile, 'w') as opf:
        for item in parse_pdb(infile):
            if isinstance(item, str):
                opf.write(item)
            elif isinstance(item, list):
                symbol = symbols[chain_count % 100]         # %100 for pdb files with > 100 chains
                opf.write(add_cid(item, symbol))
                atom_count += 1
                if atom_count % natom == 0:
                    chain_count += 1
            else:
                raise ValueError("unexpected line in {0}".format(infile))

if __name__ == "__main__":
    infile = sys.argv[1]
    outputfile = infile[:-4] + '_with_cid.pdb'
    main(infile, outputfile, 56)
