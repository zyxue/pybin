#!/scinet/gpc/tools/Python/Python262/bin/python

"""difference between g_ana_org & g_ana_basic module: analysis in this module
will have output in written to anadir"""

__all__ = ['g_energy_tmpr', 'rg', 'rg_alltrj', 'rg_CA']

def g_energy_tmpr(kwargs):
    return 'printf "14" | g_energy -f {edrf} -o {outputdir}/{pf}_tmpr_md.xvg'.format(**kwargs)

def rg_alltrj(kwargs):
    return 'printf "1" | g_gyrate -f {proxtcf} -s {tprf} -o {outputdir}/{pf}_rg_alltrj.xvg'.format(**kwargs)

def rg(kwargs):
    return 'printf "1" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {outputdir}/{pf}_rg.xvg'.format(**kwargs)

def rg_CA(kwargs):
    return 'printf "18" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {outputdir}/{pf}_rg_CA.xvg'.format(**kwargs)
