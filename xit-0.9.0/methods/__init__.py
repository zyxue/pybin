import inspect

from methods import org
from methods import fancy
from methods import basic
from methods import interactions

# collecting all the functions available
METHODS = {}
for module in [org, basic, fancy, interactions]:
    for fname in dir(module):
        f = getattr(module, fname)
        if inspect.isfunction(f):
            METHODS.update({f.func_name:f})


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
