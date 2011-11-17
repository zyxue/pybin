#!/bin/env python

import os
import glob
import fnmatch
import subprocess

"""other usual function wrappers"""

__all__ = ['g_rama']

def g_rama(kwargs):
    return 'g_rama -f {proxtcf} -s {tprf} -b {b} -o {outputdir}/{pf}_rama.xvg'.format(**kwargs)
