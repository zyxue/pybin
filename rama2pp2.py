#!/usr/bin/env python

import glob
import numpy as np
from q_acc import parse_cmd
from Mysys import read_mysys_dat

mysys = read_mysys_dat()

""" it's slow, could be improved a lot 2011-04-04"""

def outline(infile):
    with open(infile, 'r') as inf:
        calc_secondary_structures(inf)

def get_data(inf):
    for line in inf:
        if (not line.startswith('#') and 
            not line.startswith('@') and
            line.strip()):
            yield line.strip().split()[:2]

def calc_secondary_structures(inf):
    lines = np.array(list(get_data(inf)))
    # lines = np.array(get_data(inf))
    phi = lines[:,0]
    psi = lines[:,1]

    h, phip, psip = np.histogram2d(phi, psi, bins=10)
    return h, phip, psip


# def rama2pp2(infile):
#     phi = [-95, -55]                              # boundary of accpetable phi
#     psi = [125, 165]                              # boundary of acceptable psi
#     # ref: Rauscher et al. 2006
#     pp2_res = {}                                  # num of pp2 for each residues
#     opf = open('%s_pp2.xvg' % infile[:-9], 'w')
#     opf.write('# %-10s%20s\n' % ("NO.frame,", "NO.pp2 normalized by length of the peptide"))
#     last_aa = get_last_aa(infile)
#     with open(infile,'r') as inf:
#         fc = 0                                                   # frame_counter
#         pp2c = 0                                                 # ppII counter by frame
#         for line in inf:
#             if line.startswith('#') or line.startswith('@'):
#                 pass
#             else:
#                 sl = line.split()
#                 if (phi[0] < float(sl[0]) < phi[1]) and (psi[0] < float(sl[1]) < psi[1]):
#                     pp2c += 1
#                     if sl[2] in pp2_res:
#                         pp2_res[sl[2]] += 1
#                     else:
#                         pp2_res[sl[2]] = 1
#                 if sl[2] == last_aa:
#                     fc += 1
#                     opf.write('%-10d%-20d\n' % (fc, pp2c))
#                     pp2c = 0                         # reinitialize ppII counter
#     opf.close()
#     # bb = {}
#     # for k in pp2_res.keys():
#     #     bb[pp2_res[k]] = k
#     # for i in sorted(bb.keys()):
#     #     print "%10s %10d" % (bb[i], i)

if __name__ == '__main__':
    """Usage: e.g.
    rama2pp2.py -f "*rama.xvg"
    operating in the directory where *ramra.xvg files are
    """
    outline('/home/zyxue/pyfiles/dihedral_angle_analysis/test_rama.xvg')
    # infiles = sorted(glob.glob(parse_cmd().fs))
    # for inf in infiles:
    #     print inf
    #     rama2pp2(inf)
