
def rg_c_alpha(**kw):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return '''printf 'C-alpha' | g_gyrate \
-f {orderxtcf} \
-s {tprf} \
-b {b} \
-o {anal_dir}/{id_}_rg_c_alpha.xvg'''.format(**kw)

def rg_wl(**kw):
    """
    whole length rg, usually for checking convergence
    """
    return '''printf 'C-alpha' | g_gyrate \
-f {orderxtcf} \
-s {tprf} \
-b 0 \
-o {anal_dir}/{id_}_rg_wl.xvg'''.format(**kw)

def e2ed(**kw):
    """end to end distance"""
    # 2012-09-18
    # myg_dist & g_dist, the results are different for sq4m00 in mono_su_as.

    # By comparing the results in vmd, g_dist and myg_dist, as well as that
    # from g_dist on proxtcf and orderxtcf, the results returned by g_dist is
    # found to be unreliable.

    # Since my analysis is all based on orderxtcf, using g_dist would be good,
    # there is not problem concerning PBC any more.

    return """printf 'N_ter\nC_ter\n' | g_dist \
-f {orderxtcf} \
-s {tprf} \
-b {b} \
-n {ndxf} \
-o {anal_dir}/{id_}_e2ed.xvg""".format(**kw)

def e2ed_wl(**kw):
    return """printf 'N_ter\nC_ter\n' | g_dist \
-f {orderxtcf} \
-s {tprf} \
-b 0 \
-n {ndxf} \
-o {anal_dir}/{id_}_e2ed.xvg""".format(**kw)
