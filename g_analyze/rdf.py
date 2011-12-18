#!/scinet/gpc/tools/Python/Python262/bin/python

####################RDF Calculation####################

__all__ = ['rdf_unun', 'rdf_unvn', 'rdf_unvp', 'rdf_upun', 'rdf_upup',
           'rdf_upvn', 'rdf_upvp', 'rdf_vnvn', 'rdf_vpvn', 'rdf_vpvp']

uu_rdf_template = 'printf {inter_groups} | g_rdf_excl1 -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {outputdir}/{pf}_{g_tool}.xvg' # rdf within solutes
ux_rdf_template = 'printf {inter_groups} | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {outputdir}/{pf}_{g_tool}.xvg' # rdf between different molecules

def rdf_upup(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_upun(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_unun(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_upvp(kwargs):
    return ux_rdf_template.format(**kwargs)

def rdf_upvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)

def rdf_unvp(kwargs):
    return ux_rdf_template.format(**kwargs)

def rdf_unvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)

def rdf_vpvp(kwargs):
    return ux_rdf_template.format(**kwargs)

def rdf_vpvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)

def rdf_vnvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)


