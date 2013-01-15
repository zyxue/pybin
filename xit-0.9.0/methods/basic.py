
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
