#! /usr/bin/env python

import os
import shutil
import sys

with open(sys.argv[1]) as inf:
    for line in inf:
        if line.startswith('!!!'):
            cpt = line.split()[1]
            prev_cpt = cpt[:-4] + "_prev.cpt"
            assert os.path.exists(cpt) == True
            assert os.path.exists(prev_cpt) == True
            shutil.copy(prev_cpt, cpt)
