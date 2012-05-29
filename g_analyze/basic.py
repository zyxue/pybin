#!/env/bin/env python

"""

DIFFERENCE BETWEEN organization & basic MODULE:

analysis in basic module will have output written to anadir

"""

def g_energy(kwargs):
    return 'printf "Potential\nKinetic-En.\nTotal-Energy\nTemperature\nPressure\nDensity-(SI)\n" | g_energy -f {edrf} -o {anadir}/{pf}_energy.xvg'.format(**kwargs)

def rg(kwargs):
    return 'printf "Protein" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {anadir}/{pf}_rg.xvg'.format(**kwargs)

def rg_whole_length(kwargs):
    return "printf 'C-alpha' | g_gyrate -f {proxtcf} -s {tprf} -b 0 -o {anadir}/{pf}_rg_whole_length.xvg".format(**kwargs)

def rg_backbone(kwargs):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return 'printf "Backbone" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {anadir}/{pf}_rg_backbone.xvg'.format(**kwargs)

def rg_c_alpha(kwargs):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return "printf 'C-alpha' | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {anadir}/{pf}_rg_c_alpha.xvg".format(**kwargs)

def e2ed(kwargs):
    """end to end distance"""
    return "printf 'N_ter\nC_ter\n' | myg_dist -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -noxvgr -o {anadir}/{pf}_e2ed.xvg".format(**kwargs)

def dssp(kwargs):
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -b {b} -sc {anadir}/{pf}_dssp.xvg'.format(**kwargs)

def dssp_E(kwargs):
    # return 'printf "Protein" | mydo_dssp -f {xtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg -o {anadir}/{pf}_dssp_E.xpm'.format(**kwargs)
    # return 'printf "Protein" | mydo_dssp -f {proxtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg'.format(**kwargs)
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg'.format(**kwargs)

def cis_trans_pro(kwargs):
    return 'g_angle -f {proxtcf} -n ./repository/sq1_cis_trans_pro.ndx -b {b} -type dihedral -od {anadir}/{pf}_cis_trans_pro_dist.xvg -all -ov  {anadir}/{pf}_cis_trans_pro_ave.xvg '.format(**kwargs)

def peptide_bonds_dih(kwargs):
    return 'g_angle -f {proxtcf} -n /scratch/p/pomes/zyxue/mono_su_as/repository/sq2_peptide_bond_dih.ndx -type dihedral -od {anadir}/{pf}_peptide_bond_dih.xvg'.format(**kwargs)


def bonds_length(kwargs):
    return 'calc_bonds_length.py -f {xtcf} -s {grof} -b {b} -e {e} -o {anadir}/{pf}_bonds_length.xvg'.format(**kwargs)
