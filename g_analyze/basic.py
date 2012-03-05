#!/env/bin/env python

"""

DIFFERENCE BETWEEN organization & basic MODULE:

analysis in basic module will have output written to anadir

REMEMBER:

##########
When you add a new function, add the function name to __all__, too.
##########

"""

__all__ = ['g_energy_tmpr', 'rg', 'rg_backbone', 'rg_c_alpha', 'e2ed',
           'sequence_spacing', 
           'dssp_E', 'dssp_H', 'dssp_G', 'dssp_T', 'dssp_B', 'dssp_C']

def g_energy_tmpr(kwargs):
    return 'printf "14" | g_energy -f {edrf} -o {anadir}/{pf}_tmpr_md.xvg'.format(**kwargs)

def rg(kwargs):
    return 'printf "Protein" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {anadir}/{pf}_rg.xvg'.format(**kwargs)

def rg_backbone(kwargs):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return 'printf "Backbone" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_rg_backbone.xvg'.format(**kwargs)

def rg_c_alpha(kwargs):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return "printf 'C-alpha' | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {anadir}/{pf}_rg_c_alpha.xvg".format(**kwargs)

def e2ed(kwargs):
    """end to end distance"""
    return 'printf "ACE_&_CH3\nNH2_&_N" | myg_dist -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_e2ed.xvg'.format(**kwargs)

def sequence_spacing(kwargs):
    """2011-11-30: sequence_spacing.py, Andreas Vitalis, Xiaoling Wang and Rohi V.Pappu 2008 JMB"""
    return "sequence_spacing.py --pf {pf} -f {proxtcf} -s {progrof} -b {b} -l {peptide_length} -o {anadir}/{pf}_sequence_spacing.xvg".format(**kwargs)

def dssp_E(kwargs):
    # return 'printf "Protein" | mydo_dssp -f {xtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg -o {anadir}/{pf}_dssp_E.xpm'.format(**kwargs)
    # return 'printf "Protein" | mydo_dssp -f {proxtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg'.format(**kwargs)
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg'.format(**kwargs)

def dssp_H(kwargs):
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -sss H -b {b} -sc {anadir}/{pf}_dssp_H.xvg'.format(**kwargs)

def dssp_G(kwargs):
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -sss G -b {b} -sc {anadir}/{pf}_dssp_G.xvg'.format(**kwargs)

def dssp_T(kwargs):
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -sss T -b {b} -sc {anadir}/{pf}_dssp_T.xvg'.format(**kwargs)

def dssp_B(kwargs):
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -sss B -b {b} -sc {anadir}/{pf}_dssp_B.xvg'.format(**kwargs)

def dssp_C(kwargs):
    return 'printf "Protein" | ~/myg_tools/mydo_dssp/mydo_dssp -f {proxtcf} -s {tprf} -sss C -b {b} -sc {anadir}/{pf}_dssp_C.xvg'.format(**kwargs)
