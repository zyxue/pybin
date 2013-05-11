import inspect

from methods import org
from methods import fancy
from methods import basic
from methods import interactions

# uses a different way to collect methods than __init__ in plot_types, just to
# see why is better in long-term. The later one must be better for frequently
# added modules

# collecting all the functions available
TRANSFORMABLE_METHODS = {}
for module in [basic, fancy, interactions]:
    for fname in dir(module):
        f = getattr(module, fname)
        if inspect.isfunction(f):
            TRANSFORMABLE_METHODS.update({f.func_name:f})

METHODS = TRANSFORMABLE_METHODS.copy()
for fname in dir(org):
    f = getattr(org, fname)
    if inspect.isfunction(f):
        METHODS.update({f.func_name:f})
    

# JUST FOR REFERENCE 
# rg_c_alpha  = B.rg_c_alpha
# rg_wl       = B.rg_wl
# e2ed        = B.e2ed

# upup            = I.upup
# unun            = I.unun
# unun_wl         = I.unun_wl
# upup_map        = I.upup_map
# unun_map        = I.unun_map

# check_inputdir = O.check_inputdir
# g_select        = O.g_select
# symlink_ndx     = O.symlink_ndx
# extend_tpr      = O.extend_tpr
# trjconv_progrof = O.trjconv_progrof
# trjorder    = O.trjorder
