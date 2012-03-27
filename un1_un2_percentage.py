#! /usr/bin/env python

import os
from Bio import SeqIO

#   Primary        Secondary        Tertiary        bbpC        scnC            
# G 		   1(Ca)                            3(N, C, O)  0
# V 2(Cy1, Cy2)			    2(Ca, Cb)       3(N, C, O)  3(Cb, Cy1, Cy2)
# P		   3(Cb, Cy, Cd)                    3(N, C, O)  3(Cb, Cy, Cd)
# A 1(Cb)			    1(Ca)           3(N, C, O)  1(Cb)
# Q 	           2(Cb, Cy)	    1(Ca)           3(N, C, O)  2(Cb, Cy)

UN1 = {
    'C1' : {'A': 1,
            'V': 2,},
    'C2' : {'G': 1,
            'P': 3,
            'Q': 2,},
    'C3' : {'P': 1,
            'A': 1,
            'V': 2,
            'Q': 1},
    }
UN2 = {
    'C1' : {'A': 1,
            'V': 2,},
    'C2' : {'P': 3,
            'Q': 2,},
    'C3' : {'V': 1},
    }
UN3 = {
    'C1' : {'A': 1,
            'V': 2,},
    'C2' : {'G': 1,
            'P': 3,
            'Q': 2,},
    'C3' : {},
    }

def main():
    seq_file = os.path.join(os.environ['HOME'], 'pybin/mysys/myseqs.fasta')
    UN1_selection, UN2_selection, UN3_selection = {}, {}, {}
#     UN1C1, UN1C2, UN1C3, UN2C1, UN2C2, UN2C3 = {}, {}, {}, {}, {}, {}
    for seq in SeqIO.parse(seq_file, 'fasta'):
        UN1_selection[seq.description] = {}
        UN2_selection[seq.description] = {}
        UN3_selection[seq.description] = {}
        for C in ['C1', 'C2', 'C3']:
            UN1_selection[seq.description][C] = sum(
                UN1[C].get(aa, 0) * seq.seq.count(aa)
                for aa in list('GPVAQ')
                )

            UN2_selection[seq.description][C] = sum(
                UN2[C].get(aa, 0) * seq.seq.count(aa)
                for aa in list('GPVAQ')
                )

            UN3_selection[seq.description][C] = sum(
                UN3[C].get(aa, 0) * seq.seq.count(aa)
                for aa in list('GPVAQ')
                )


    printf(UN1_selection, UN2_selection, UN3_selection)

def printf(UN1_selection, UN2_selection, UN3_selection):
    print "{0:>15s},{1:>15s},{2:>15s},{3:>15s}\n".format(
        '', 'C1', 'C2', 'C3'),
    for seq in sorted(UN1_selection.keys()):
        for selection in [UN1_selection, UN2_selection, UN3_selection]:
            un = sum(selection[seq].values())
            c1 = float(selection[seq]['C1'])
            c2 = float(selection[seq]['C2'])
            c3 = float(selection[seq]['C3'])
            if un != 0:
                c1_p = c1/un                           # c1_p: c1 in percentage
                c2_p = c2/un
                c3_p = c3/un
                print "{0:15s},{1:15.2f},{2:15.2f},{3:15.2f}\n".format(
                    seq, c1_p, c2_p, c3_p),
            else:
                print '-' * 60

if __name__ == "__main__":
    main()
