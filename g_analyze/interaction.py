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

"""THE FOLLOWING FUNCTIONS HAVE TO BE SEPARATED BECAUSE THEIR RETURN VALUES
CONTAIN THE __NAME__ OF THE FUNCTION"""

####################UUI####################
def upup(kwargs): # dDA < 3.5nm & angle ADH<30 degree, which is the default criteria in gromacs 4.0.7
    return 'printf "Protein_no_end\nProtein_no_end\n" | g_hbond -f {proxtcf} -s {tprf} -n {ndxf} -b {b} -r 0.35 -nonitacc -num {anadir}/{pf}_upup.xvg'.format(**kwargs)

def upup60(kwargs): # dDA < 3.5nm & angle ADH<30 degree, which is the default criteria in gromacs 4.0.7
    return 'printf "1\n1" | myg_hbond -f {xtcf} -s {tprf} -b {b} -r 3.5 -a 60 -nonitacc \
-num {anadir}/{pf}_upup60.xvg \
-dist {anadir}/{pf}_upup60_dist.xvg \
-ang {anadir}/{pf}_upup60_ang.xvg \
-hx {anadir}/{pf}_upup60_hx2.xvg \
-hbm {anadir}/{pf}_upup60_hbm.xvg \
-hbn {anadir}/{pf}_upup60_hbn.xvg'.format(**kwargs)

# def upun(kwargs):
#     return uu_nonhb_template.format(**kwargs)

def unun(kwargs):
    return 'printf "UN3\nUN3\n" | g_mindist_excl1 -f {proxtcf} -s {progrof} -n {ndxf} -b {b}  -e {e} -d 0.55 -on {anadir}/{pf}_unun.xvg -od {anadir}/{pf}_mindist.xvg'.format(**kwargs)
    # return 'unun.py -f {proxtcf} -s {progrof} -b {b} -c 0.55 -o {anadir}/{pf}_unun.xvg'.format(**kwargs)

####################UVI####################
def upvp(kwargs):
    return 'printf "Protein_no_end\nSolvent\n" | g_hbond -f {centerxtcf} -s {tprf} -n {ndxf} -b {b} -e {e} -r 0.35 -nonitacc -num {anadir}/{pf}_upup.xvg'.format(**kwargs)

    # if kwargs.has_key('hb_tprf'):
    #     kwargs['tprf'] = kwargs['hb_tprf']
    # return uv_hb_template.format(**kwargs)

def upvn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'pwd'
    return 'printf "UP\nVN\n" | g_mindist_excl1 -f {centerxtcf} -s {tprf} -n {ndxf} -b {b} -e {e} -d 0.45 -on {anadir}/{pf}_upvn.xvg -od {anadir}/{pf}_mindist.xvg'.format(**kwargs)

def unvp(kwargs):
    return 'printf "UN\nVP\n" | g_mindist_excl1 -f {centerxtcf} -s {tprf} -n {ndxf} -b {b} -e {e} -d 0.45 -on {anadir}/{pf}_unvp.xvg -od {anadir}/{pf}_mindist.xvg'.format(**kwargs)

def unvn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'pwd'
    return 'printf "UN\nVN\n" | g_mindist_excl1 -f {centerxtcf} -s {tprf} -n {ndxf} -b {b} -e {e} -d 0.45 -on {anadir}/{pf}_unvn.xvg -od {anadir}/{pf}_mindist.xvg'.format(**kwargs)

####################VVI####################
def vpvp(kwargs):
    pass

def vpvn(kwargs):
    pass

def vnvn(kwargs):
    pass
