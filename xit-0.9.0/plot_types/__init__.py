import inspect

from utils import timeit

import alx
import bar
import distr
import map_
import grped_bars

PLOT_TYPES = {}
for module in [alx, bar, distr, map_, grped_bars]:
    for fname in dir(module):
        f = getattr(module, fname)
        if inspect.isfunction(f):
            PLOT_TYPES.update({f.func_name: timeit(f)})

# JUST FOR REFERENCE 
# alx = A.alx
# simple_bar = B.simple_bar
# distr = D.distr
# pmf   = D.pmf
# map   = timeit(M.map_)
