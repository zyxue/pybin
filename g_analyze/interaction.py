#!/usr/bin/env python

"""

This file includes files that are relevant to analyzing different types of
interaction.

NOTE: PROBABLY THIS FILE WILL BE REWRITTEN!!! 2011-11-18

OPTIONS FOR OUTPUT FILES:
-dist # distance distribution of hydrogen bonds               
-ang  # angle distribution of HB                              
-hx   # number of n-n+i HB as a function of time, 0 <= i <= 6 
-hbn  # existence matriz for all hydrogen bonds over all
-hbm  # index for hbm, useful if you want to draw the map
"""

__all__ = ['unun', 'upup', 'upun', 
           'unvn', 'unvp', 'upvn', 'upvp', 
           'vnvn', 'vpvn', 'vpvp',
           'upup60']

igmat = {                      # interaction groups matrix 
    # commented means nolonger correct!
    # 'upup':'"16\n16"',
    # 'upun':'"16\n17"',
    # 'unun':'"17\n17"',

    'upvp': ' 1\n12',                                           # needs hydrogen to calculate HB
    'upvn': '14\n17',
    'unvp': '15\n16',
    'unvn': '15\n17',
    
    # commented means nolonger correct!
    # 'vpvp':'"14\n14"',
    # 'vpvn':'"14\n15"',
    # 'vnvn':'"15\n15'
    }

icmat = {                                            # interaction cutoff matrix
    'upup':0.35,'upun':0.44,'unun':0.53,
    'upvp':0.35,'upvn':0.44,'unvp':0.44,'unvn':0.53,
    'vpvp':0.35,'vpvn':0.44,'vnvn':0.53
    }

hb_template = '-s {tprf} -b {b} -r {ic:.2f} -nonitacc -num {anadir}/{pf}_{tinter}.xvg'

# uu_hb_template = 'printf "1\n1" | g_hbond -f {{proxtcf}} {hb_template}'.format(hb_template=hb_template)
uv_hb_template = 'printf "{{igrp}}" | g_hbond -f {{xtcf}} {hb_template}'.format(hb_template=hb_template)
# vv_hb_template = 'printf "12\n12" | g_hbond -f {{xtcf}} {hb_template}'.format(hb_template=hb_template)


# uu_nonhb_template = 'printf {igrp} | g_mindist_excl1 -f {proxtcf} -s {tprf} -n {ndxf} -b {b} -d {ic:.2f} -on {anadir}/{pf}_{tinter}.xvg -od {anadir}/tmp_{pf}.xvg'

ux_nonhb_template = 'printf "{igrp}" | g_mindist -f {xtcf} -s {tprf} -n {ndxf} -b {b} -d {ic:.2f} -on {anadir}/{pf}_{tinter}.xvg -od {anadir}/tmp_{pf}.xvg'

"""THE FOLLOWING FUNCTIONS HAVE TO BE SEPARATED BECAUSE THEIR RETURN VALUES
CONTAIN THE __NAME__ OF THE FUNCTION"""

####################UUI####################
def upup(kwargs): # dDA < 3.5nm & angle ADH<30 degree, which is the default criteria in gromacs 4.0.7
    if kwargs.has_key('hb_tprf'):
        kwargs['tprf'] = kwargs['hb_tprf']
    return uu_hb_template.format(**kwargs)

def upup60(kwargs): # dDA < 3.5nm & angle ADH<30 degree, which is the default criteria in gromacs 4.0.7
    return 'printf "1\n1" | myg_hbond -f {xtcf} -s {tprf} -b {b} -r 3.5 -a 60 -nonitacc \
-num {anadir}/{pf}_upup60.xvg \
-dist {anadir}/{pf}_upup60_dist.xvg \
-ang {anadir}/{pf}_upup60_ang.xvg \
-hx {anadir}/{pf}_upup60_hx2.xvg \
-hbm {anadir}/{pf}_upup60_hbm.xvg \
-hbn {anadir}/{pf}_upup60_hbn.xvg'.format(**kwargs)

def upun(kwargs):
    return uu_nonhb_template.format(**kwargs)

def unun(kwargs):
    return 'unun.py -f {proxtcf} -s {progrof} -b {b} -c 0.53 -o {anadir}/{pf}_unun.xvg'.format(**kwargs)

####################UVI####################
def upvp(kwargs):
    kwargs['igrp'] = igmat['upvp']
    kwargs['tinter'] = 'upvp'
    kwargs['ic'] = icmat['upvp']
    if kwargs.has_key('hb_tprf'):
        kwargs['tprf'] = kwargs['hb_tprf']
    return uv_hb_template.format(**kwargs)

def upvn(kwargs):
    kwargs['igrp'] = igmat['upvn']
    kwargs['tinter'] = 'upvn'
    kwargs['ic'] = icmat['upvn']
    return 'echo' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)

def unvp(kwargs):
    kwargs['igrp'] = igmat['unvp']
    kwargs['tinter'] = 'unvp'
    kwargs['ic'] = icmat['unvp']
    # Check how pbc works in gromacs and then do this
    return ux_nonhb_template.format(**kwargs)

def unvn(kwargs):
    kwargs['igrp'] = igmat['unvn']
    kwargs['tinter'] = 'unvn'
    kwargs['ic'] = icmat['unvn']
    return 'echo' if kwargs['cdt'] == 'w' else ux_nonhb_template .format(**kwargs) 

####################VVI####################
def vpvp(kwargs):
    return vv_hb_template.format(**kwargs)

def vpvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)

def vnvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)
