#! /usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator #, FormatStrFormatter
import Bio
# from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='infile', default=None, required=True,
                             help='specify the input fasta file')
parser.add_argument('-o', dest='outputfile', default=None,
                    help='specify the output png file, if not specified, plt.show()')
args = parser.parse_args()

seqio = Bio.SeqIO.parse(args.infile, 'fasta')
aas = Bio.Alphabet.IUPAC.IUPACProtein.letters

aas_count = {}
for seq in seqio:
    aas_count[seq.description] = {}
    for aa in aas:
        l_seq = len(seq.seq)
        aas_count[seq.description][aa] = seq.seq.count(aa) / float(l_seq)

from pprint import pprint as pp

pp(aas_count)

aas_list = aas_count[aas_count.keys()[0]].keys()
aas2int = {}
for k, aa in enumerate(aas_list):
    print k, aa
    aas2int[aa] = k
    
fig = plt.figure()
ax = fig.add_subplot(111)    
for k in aas_count:
    x = [aas2int[aa] for aa in aas_list]
    y = [aas_count[k][aa] for aa in aas_list]
    ax.plot(x, y, '-o', linewidth=1, label=k)

majorLocator = MultipleLocator(1)
ax.xaxis.set_major_locator(majorLocator)
xtickNames = plt.setp(ax, xticklabels=[''] + aas_list)
# plt.setp(xtickNames, rotation=45, fontsize=8)

ax.grid(which='both')
ax.set_xlim([-1, 20])
plt.legend(loc='best')
if args.outputfile:
    plt.savefig(args.outputfile)
else:
    plt.show()
