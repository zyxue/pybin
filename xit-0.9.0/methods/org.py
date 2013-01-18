import os

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
