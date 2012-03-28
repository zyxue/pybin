#! /usr/bin/env python

import os
from Bio import SeqIO

#   Primary        Secondary        Tertiary      scnC            bbpC      
# G 		   1(Ca)                          0               3(N, C, O)
# P		   3(Cb, Cy, Cd)    1(Ca)         3(Cb, Cy, Cd)   3(N, C, O)
# A 1(Cb)			    1(Ca)         1(Cb)           3(N, C, O)
# V 2(Cy1, Cy2)			    2(Ca, Cb)     3(Cb, Cy1, Cy2) 3(N, C, O)
# Q 	           2(Cb, Cy)	    1(Ca)         2(Cb, Cy)       3(N, C, O)

# bbpC: backbone polar Carbon
# scnC: sidechain nonpolar Carbon

atoms_dd = {
    'primary'  : {'A': 1,                                     # Cb
                  'V': 2,},                                   # Cy1, Cy2
    'secondary': {'G': 1,                                     # Ca
                  'P': 3,                                     # Cb, Cy, Cd
                  'Q': 2,},                                   # Cb, Cy
    'tertiary' : {'P': 1,                                     # Ca
                  'A': 1,                                     # Ca
                  'V': 2,                                     # Ca, Cb
                  'Q': 1},                                    # Ca        
    'patoms'   : {'P': 3,                                     # polar atoms
                  'A': 3,
                  'G': 3,
                  'V': 3,
                  'Q': 3},
    'scnC'    : {'G': 0,
                 'P': 3,
                 'A': 1,
                 'V': 3,
                 'Q': 2},
    # not sure how should that of Q be counted 2012-03-09
#     'hbg'     : {'G': 2,
#                  'P': 2,
#                  'A': 2,
#                  'V': 2,
#                  'P': 1}
    }

HYDROPATHY_DD = {
    'V': 4.2,
    'A': 1.8,
    'G': -0.4,
    'P': -1.6,
    'Q': -3.5,
    }

def main():
    seq_file = os.path.join(os.environ['HOME'], 'pybin/myseqs.fasta')
    primary, secondary, tertiary, HBgroup, patoms, scnC, hydropathy = {}, {}, {}, {}, {}, {}, {}
    for seq in SeqIO.parse(seq_file, 'fasta'):
        primary[seq.description] = sum(
            atoms_dd['primary'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        secondary[seq.description] = sum(
            atoms_dd['secondary'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        tertiary[seq.description] = sum(
            atoms_dd['tertiary'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        patoms[seq.description] = sum(
            atoms_dd['patoms'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        scnC[seq.description] = sum(
            atoms_dd['scnC'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        # Since the N of Pro cannot form HB, and only backbone HBgroups are counted
        HBgroup[seq.description] = 2 * len(seq) - seq.seq.count('P')

        hydropathy[seq.description] = sum(
            HYDROPATHY_DD.get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

#     from pprint import pprint as pp
#     pp(primary)
#     pp(secondary)
#     pp(tertiary)
    printf(primary, secondary, tertiary, HBgroup, patoms, scnC, hydropathy)

def printf(primary, secondary, tertiary, HBgroup, patoms, scnC, hydropathy):
    print "#" * 79, "\n"

    print ("# all_nC  : all nonpolar carbons (including CA)\n"
           "# all_scnC: all sidechain nonpolar carbons (exception: for (G)35, CA is used instead)\n"
           "# all 12C : all primary and secondary carbons\n"
           "# HBg     : hydrogen bonding groups\n"
           "# patoms  : polar atoms"
           "\n")
    print "#" * 79, "\n"

    print "{0:>15s},{1:>15s},{2:>15s},{3:>15s},{4:>15s},{5:>15s}{6:>15s}\n".format(
        '', 'all_nC', 'all_scnC', 'all_12C', 'HBg', 'patoms(C,O,N)', 'KDhydropathy'),
    for seq in sorted(primary.keys()):
        # the two ends are always not counted
        print "{0:15s},{1:15d},{2:15d},{3:15d},{4:15d},{5:15d}{6:15.1f}\n".format(
            seq, 
            primary[seq] + secondary[seq] + tertiary[seq],
            scnC[seq],
            primary[seq] + secondary[seq],
            HBgroup[seq],
            patoms[seq],
            hydropathy[seq]),
        

if __name__ == "__main__":
    main()
