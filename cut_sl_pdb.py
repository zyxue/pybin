#! /usr/bin/env python

"""This script is to cut superlong peptides into shorter fragments""" 

import argparse

def parse_cmd():
    """parse_cmd"""
    parser = argparse.ArgumentParser(description='This script is to cut superlong peptides into shorter fragments')
    parser.add_argument('-f', dest='inputfile', required=True,
                        help="specify the structure file of the super long peptide")
    parser.add_argument('-o', dest='outputfile', default='out.gro',
                        help="specify the outputfile name ")
    parser.add_argument('-l', dest='ppl', required=True, 
                        help='peptide length (e.g. 35)')
    args = parser.parse_args()
    return args


def main():
    """ppl: peptide length"""
    args = parse_cmd()
    inputfile = args.inputfile
    outputfile = args.outputfile
    ppl = int(args.ppl)

    opf = open(outputfile, 'w')
    
    ppl = ppl + 2 -1                                       # considering the first C-ter ACE (it's simple math)
    with open(inputfile) as inf:
        # read the first two lines
        opf.write(inf.readline())                           # copy first line
        opf.write(inf.readline())                           # copy second line

        # start processing the main body of gro file
        for line in inf:
            resid = line[:5].strip()
            resname = line[5:8].strip()
            name = line[8:15].strip()
            id_ = line[15:20].strip()
            x = line[20:28].strip()
            y = line[28:36].strip()
            z = line[36:44].strip()
            # print id_, x, y, z

            # trying to pass the last line, which shows box size
            if not resname.isalpha():
                opf.write(line)                           # copy the last line
            else:
                # (1 + ppl * k) is the resid of linking GLY (math)
                resid_minus_one = int(resid) - 1
                if (resname == 'ACE' or                     # first residue
                    resname == 'NH2' or                     # last residue
                    resid_minus_one % ppl != 0):            # middle but not linking GLY
                    new_resid = 1 + resid_minus_one % ppl
                    write_to_gro(str(new_resid), resname, name, id_, x, y, z, opf)
                else:
                    # How the linking GLY will be split into NH2 and GLY
                    change_dd = {
                        'N':  [int(resid), 'NH2', 'N'],
                        'CA': [int(resid) + 1, 'ACE', 'CH3'],
                        'C':  [int(resid) + 1, 'ACE', 'C'],
                        'O':  [int(resid) + 1, 'ACE', 'O']
                        }

                    new_resid, new_resname, new_name = change_dd[name]
                    
                    write_to_gro(str(new_resid), new_resname, new_name, id_, x, y, z, opf)
    opf.close()

def write_to_gro(resid, resname, name, id_, x, y, z, opf):
    opf.write('{0:>5s}{1:3s}{2:>7s}{3:>5s}{4:>8s}{5:>8s}{6:>8s}\n'.format(
        resid, resname, name, id_, x, y, z
        ))

if __name__ == "__main__":
    main()
