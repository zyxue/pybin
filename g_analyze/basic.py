#!/env/bin/env python

"""

DIFFERENCE BETWEEN organization & basic MODULE:

analysis in basic module will have output written to anadir

REMEMBER:

##########
When you add a new function, add the function name to __all__, too.
##########

"""

__all__ = ['g_energy_tmpr', 'rg_alltrj', 'rg', 'rg_backbone', 'e2ed']

def g_energy_tmpr(kwargs):
    return 'printf "14" | g_energy -f {edrf} -o {anadir}/{pf}_tmpr_md.xvg'.format(**kwargs)

def rg_alltrj(kwargs):
    return 'printf "Protein" | g_gyrate -f {proxtcf} -s {tprf} -o {anadir}/{pf}_rg_alltrj.xvg'.format(**kwargs)

def rg(kwargs):
    return 'printf "Protein" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {anadir}/{pf}_rg.xvg'.format(**kwargs)

def rg_backbone(kwargs):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return 'printf "Backbone" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_rg_backbone.xvg'.format(**kwargs)

def e2ed(kwargs):
    """end to end distance"""
    return 'printf "ACE_&_CH3\nNH2_&_N" | myg_dist -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_e2ed.xvg'.format(**kwargs)
