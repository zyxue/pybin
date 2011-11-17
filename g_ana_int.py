#!/usr/bin/env python

__all__ = ['unun', 'unvn', 'unvp', 'upun', 'upup', 'upvn', 'upvp', 'vnvn', 'vpvn', 'vpvp']

def inter_groups_matrix():
    igm = {
        'upup':'"16\n16"','upun':'"16\n17"','unun':'"17\n17"',
        'upvp':'"16\n14"','upvn':'"16\n15"','unvp':'"17\n14"','unvn':'"17\n15"',
        'vpvp':'"14\n14"','vpvn':'"14\n15"','vnvn':'"15\n15'
        }                                                # interaction matrix groups
    return igm

def inter_cutoffs():
    ic = {
        'upup':0.35,'upun':0.44,'unun':0.53,
        'upvp':0.35,'upvn':0.44,'unvp':0.44,'unvn':0.53,
        'vpvp':0.35,'vpvn':0.44,'vnvn':0.53
        }
    return ic

hb_template = '-s {tprf} -b {b} -r {icff:.2f} -nonitacc -num {outputdir}/{pf}_{g_tool}.xvg'

uu_hb_template = 'printf "1\n1" | g_hbond -f {{proxtcf}} {hb_template}'.format(hb_template=hb_template)
uv_hb_template = 'printf "1\n12" | g_hbond -f {{xtcf}} {hb_template}'.format(hb_template=hb_template)
vv_hb_template = 'printf "12\n12" | g_hbond -f {{xtcf}} {hb_template}'.format(hb_template=hb_template)

uu_nonhb_template = 'printf {igrp} | g_mindist_excl1 -f {proxtcf} -s {tprf} -n {ndxf} -b {b} -d {icff:.2f} -on {outputdir}/{pf}_{g_tool}.xvg -od {outputdir}/tmp_{pf}.xvg'
ux_nonhb_template = 'printf {igrp} | g_mindist_excl1 -f {xtcf}    -s {tprf} -n {ndxf} -b {b} -d {icff:.2f} -on {outputdir}/{pf}_{g_tool}.xvg -od {outputdir}/tmp_{pf}.xvg'

"""THE FOLLOWING FUNCTIONS HAVE TO BE SEPARATED BECAUSE THEIR RETURN VALUES
CONTAIN THE __NAME__ OF THE FUNCTION"""

####################UUI####################
def upup(kwargs): # dDA < 3.5nm & angle ADH<30 degree, which is the default criteria in gromacs 4.0.7
    if kwargs.has_key('hb_tprf'):
        kwargs['tprf'] = kwargs['hb_tprf']
    return uu_hb_template.format(**kwargs)

def upun(kwargs):
    return uu_nonhb_template.format(**kwargs)

def unun(kwargs):
    return uu_nonhb_template.format(**kwargs)

####################UVI####################
def upvp(kwargs):
    if kwargs.has_key('hb_tprf'):
        kwargs['tprf'] = kwargs['hb_tprf']
    return uv_hb_template.format(**kwargs)

def upvn(kwargs):
    return 'echo' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)

def unvp(kwargs):
    return ux_nonhb_template.format(**kwargs)

def unvn(kwargs):
    return 'echo' if kwargs['cdt'] == 'w' else ux_nonhb_template .format(**kwargs) 

####################VVI####################
def vpvp(kwargs):
    return vv_hb_template.format(**kwargs)

def vpvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)

def vnvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)
