#! /usr/bin/env python

import os
from Bio import SeqIO

#   Primary        Secondary        Tertiary        bbpC        scnC            
# G 		   1(Ca)                            3(N, C, O)  0
# V 2(Cy1, Cy2)			    2(Ca, Cb)       3(N, C, O)  3(Cb, Cy1, Cy2)
# P		   3(Cb, Cy, Cd)    1(Ca)           3(N, C, O)  3(Cb, Cy, Cd)
# A 1(Cb)			    1(Ca)           3(N, C, O)  1(Cb)
# Q 	           2(Cb, Cy)	    1(Ca)           3(N, C, O)  2(Cb, Cy)

nonpolar_carbon_DD = {
    'primary'  : {'A': 1,                                     # Cb
                  'V': 2,},                                   # Cy1, Cy2
    'secondary': {'G': 1,                                     # Ca
                  'P': 3,                                     # Cb, Cy, Cd
                  'Q': 2,},                                   # Cb, Cy
    'tertiary' : {'P': 1,                                     # Ca
                  'A': 1,                                     # Ca
                  'V': 2,                                     # Ca, Cb
                  'Q': 1},                                    # Ca
    'patoms'   : {'P': 3,
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

def main():
    seq_file = os.path.join(os.environ['HOME'], 'pybin/mysys/myseqs.fasta')
    primary, secondary, tertiary, HBgroup, patoms, scnC = {}, {}, {}, {}, {}, {}
    for seq in SeqIO.parse(seq_file, 'fasta'):
        primary[seq.description] = sum(
            nonpolar_carbon_DD['primary'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        secondary[seq.description] = sum(
            nonpolar_carbon_DD['secondary'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        tertiary[seq.description] = sum(
            nonpolar_carbon_DD['tertiary'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        patoms[seq.description] = sum(
            nonpolar_carbon_DD['patoms'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        scnC[seq.description] = sum(
            nonpolar_carbon_DD['scnC'].get(aa, 0) * seq.seq.count(aa)
            for aa in list('GPVAQ')
            )

        print scnC[seq.description]

        # Since the N of Pro cannot form HB, and only backbone HBgroups are counted
        HBgroup[seq.description] = 2 * len(seq) - seq.seq.count('P')

#     from pprint import pprint as pp
#     pp(primary)
#     pp(secondary)
#     pp(tertiary)
    printf(primary, secondary, tertiary, HBgroup, patoms, scnC)

def printf(primary, secondary, tertiary, HBgroup, patoms, scnC):
#     print "{0:15s}{1:15s}{2:15s}{3:15s}{4:15s}\n".format(
    print "{0:>15s},{1:>15s},{2:>15s},{3:>15s},{4:>15s}\n".format(
        '', 'all_NP_C', 'all_scnC', 'all_1_2 C', 'HBgroup'),
    for seq in sorted(primary.keys()):
        # forget about the two ends
#         print "{0:<15s}{1:<15d}{2:<15d}{3:<15d}{4:<15d}\n".format(
        print "{0:15s},{1:15d},{2:15d},{3:15d},{4:15d}\n".format(
            seq, 
            primary[seq] + secondary[seq] + tertiary[seq],
            scnC[seq],
            primary[seq] + secondary[seq],
            HBgroup[seq]),

if __name__ == "__main__":
    main()
