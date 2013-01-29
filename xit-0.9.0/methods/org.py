import os

def trjorder(**kw):
    fn = '_{0}'.format(os.path.basename(kw['orderxtcf']))
    kw['tmporderf'] = os.path.join(kw['inputdir'], fn)

    return """
printf "Protein\nSystem\n"     | trjconv  -f {xtcf}        -s {tprf} -center   -pbc mol -ur tric -o {centerxtcf}
printf "Protein\nAll_Solvent\n"| trjorder -f {centerxtcf}  -s {tprf} -n {ndxf} -na {NA} -o {tmporderf} ;        rm {centerxtcf}
printf "Ordered_Sys\n"         | trjconv  -f {tmporderf}   -s {tprf} -n {ndxf} -o {orderxtcf};                  rm {tmporderf}
printf "Ordered_Sys\n"         | trjconv  -f {orderxtcf}   -s {tprf} -n {ndxf} -dump {b} -o {ordergrof}
""".format(**kw)


def g_select(**kw):
    CG = kw['C']['g_select']
    ndx_fn = CG['repo_ndx_tmpl'].format(**kw)
    kw['repo_ndx'] = os.path.join(kw['root'], kw['C']['data']['repository'], ndx_fn)
    gssk = CG['g_sel_sel_key_tmpl'].format(**kw)
    kw['g_sel_sel'] = CG[gssk]
    return """g_select \
-f {grof} \
-s {tprf} \
-on {repo_ndx} \
-select '{g_sel_sel}'""".format(**kw)

def symlink_ndx(**kw):
    CG = kw['C']['g_select']
    ndx_fn = CG['repo_ndx_tmpl'].format(**kw)
    kw['repo_ndx'] = os.path.join(kw['root'], kw['C']['data']['repository'], ndx_fn)

    return "ln -s -f -v {repo_ndx} {ndxf}".format(**kw)
