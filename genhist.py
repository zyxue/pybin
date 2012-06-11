#! /usr/bin/env python

import sys

import numpy as np
# scitools is has very limited ability, not as flexible as gnuplot at all
# from scitools.aplotter import plot

from xvg2png import xvg2array

infile = sys.argv[1]
x, y = xvg2array(infile)

minx, maxx = min(y), max(y)
bins = np.linspace(minx, maxx, 50)

# beg, end, step = [float(i) for i in sys.argv[2:5]]
bins = np.arange(0.6, 3.0, 0.02)

x, y = xvg2array(infile)
n, b = np.histogram(y, bins=bins, normed=False)

n = n / float(len(y))
b = (b[:-1] + b[1:]) / 2

for bi, ni in zip(b, n):
    print bi, ni

# print "NO. of bins: {0}; NO. of n: {1}".format(len(b), len(n))
# plot(b, n)
