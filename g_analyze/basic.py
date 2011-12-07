#!/env/bin/env python

"""

DIFFERENCE BETWEEN organization & basic MODULE:

analysis in basic module will have output written to anadir

REMEMBER:

##########
When you add a new function, add the function name to __all__, too.
##########

"""

__all__ = ['g_energy_tmpr', 'rg', 'rg_backbone', 'e2ed', 'rg_backbone_v', 'e2ed_v',
           'sequence_spacing', 'do_dssp_E']

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
    return "printf 'C-alpha' | g_gyrate -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_rg_backbone.xvg".format(**kwargs)

def e2ed(kwargs):
    """end to end distance"""
    return 'printf "ACE_&_CH3\nNH2_&_N" | myg_dist -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_e2ed.xvg'.format(**kwargs)

def sequence_spacing(kwargs):
    """2011-11-30: sequence_spacing.py, Andreas Vitalis, Xiaoling Wang and Rohi V.Pappu 2008 JMB"""
    return 'sequence_spacing.py --pf {pf} -f {xtcf} -s {grof} -l {peptide_length} -o {anadir}/{pf}_sequence_spacing.xvg'.format(**kwargs)

def do_dssp_E(kwargs):
    return 'printf "Protein" | do_dssp -f {xtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg -o {anadir}/{pf}_dssp_E.xpm'.format(**kwargs)
