#!/scinet/gpc/tools/Python/Python262/bin/python

####################RDF Calculation####################

__all__ = ['rdf_unun', 'rdf_upun', 'rdf_upup',
           'rdf_unvn', 'rdf_unvp', 'rdf_upvn', 'rdf_upvp', 
           'rdf_vnvn', 'rdf_vpvn', 'rdf_vpvp']

inter_groups_matrix = {
    # commented means nolonger correct!
    # 'upup':'"16\n16"',
    # 'upun':'"16\n17"',
    # 'unun':'"17\n17"',

    'upvp': '14\n16',
    'upvn': '14\n17',
    'unvp': '15\n16',
    'unvn': '15\n17',
    
    # commented means nolonger correct!
    # 'vpvp':'"14\n14"',
    # 'vpvn':'"14\n15"',
    # 'vnvn':'"15\n15'
    }                                                # interaction matrix groups

uu_rdf_template = 'printf "{inter_groups}" | g_rdf_excl1 -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {outputdir}/{pf}_{type_of_rdf}.xvg' # rdf within solutes

ux_rdf_template = 'printf "{inter_groups}" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_{type_of_rdf}.xvg' # rdf between different molecules

def rdf_upup(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_upun(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_unun(kwargs):
    return uu_rdf_template.format(**kwargs)

####################

def rdf_upvp(kwargs):
    kwargs['inter_groups'] = inter_groups_matrix['upvp']
    kwargs['type_of_rdf'] = 'rdf_upvp'
    return ux_rdf_template.format(**kwargs)

def rdf_upvn(kwargs):
    kwargs['inter_groups'] = inter_groups_matrix['upvn']
    kwargs['type_of_rdf'] = 'rdf_upvn'
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)

def rdf_un1vp(kwargs):
    return 'printf "UN1\nVP\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_un1vp.xvg'.format(**kwargs)

def rdf_un2vp(kwargs):
    return 'printf "UN2\nVP\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_un2vp.xvg'.format(**kwargs)

def rdf_un3vp(kwargs):
    return 'printf "UN3\nVP\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_un3vp.xvg'.format(**kwargs)

def rdf_un1vn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'echo cdt is w, no rdf_un1vn'
    else:
        return 'printf "UN1\nVN\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_un1vn.xvg'.format(**kwargs)

def rdf_un2vn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'echo cdt is w, no rdf_un2vn'
    else:
        return 'printf "UN2\nVN\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_un2vn.xvg'.format(**kwargs)

def rdf_un3vn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'echo cdt is w, no rdf_un3vn'
    else:
        return 'printf "UN3\nVN\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_un3vn.xvg'.format(**kwargs)

def rdf_un4vn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'echo cdt is w, no rdf_un4vn'
    else:
        return 'printf "UN4\nVN\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_un4vn.xvg'.format(**kwargs)

###############################################################################
# Below, For checking primary, secondary, tertiary carbons, individually
###############################################################################
def rdf_c1vp(kwargs):
    return 'printf "C1\nVP\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c1vp.xvg'.format(**kwargs)
    # return 'printf "C1\nVP\n" | g_rdf -f {orderxtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c1vp.xvg'.format(**kwargs)

def rdf_c2vp(kwargs):
    return 'printf "C2\nVP\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c2vp.xvg'.format(**kwargs)
    # return 'printf "C2\nVP\n" | g_rdf -f {orderxtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c2vp.xvg'.format(**kwargs)

def rdf_c3vp(kwargs):
    return 'printf "C3\nVP\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c3vp.xvg'.format(**kwargs)
    # return 'printf "C3\nVP\n" | g_rdf -f {orderxtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c3vp.xvg'.format(**kwargs)

def rdf_c1vn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'echo cdt is w, no rdf_c1vn'
    else:
        return 'printf "C1\nVN\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c1vn.xvg'.format(**kwargs)
        # return 'printf "C1\nVN\n" | g_rdf -f {orderxtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c1vn.xvg'.format(**kwargs)

def rdf_c2vn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'echo cdt is w, no rdf_c2vn'
    else:
        return 'printf "C2\nVN\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c2vn.xvg'.format(**kwargs)
        # return 'printf "C2\nVN\n" | g_rdf -f {orderxtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c2vn.xvg'.format(**kwargs)

def rdf_c3vn(kwargs):
    if kwargs['cdt'] == 'w':
        return 'echo cdt is w, no rdf_c3vn'
    else:
        return 'printf "C3\nVN\n" | g_rdf -f {xtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c3vn.xvg'.format(**kwargs)
        # return 'printf "C3\nVN\n" | g_rdf -f {orderxtcf} -s {tprf} -b {b} -e {e} -n {ndxf} -bin 0.02 -o {anadir}/{pf}_rdf_c3vn.xvg'.format(**kwargs)

###############################################################################
# Above, For checking primary, secondary, tertiary carbons, individually
###############################################################################
