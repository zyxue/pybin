#!/usr/bin/env python

import sys
import numpy as np
from xvg2png import xvg2array 

f = sys.argv[1]
x, y = xvg2array(f)
print "{0:40s}{1}".format(f, np.average(y))
