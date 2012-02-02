#! /usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', type=int, dest="npep", default=40)
parser.add_argument('-w', type=int, dest="nwater", default=240)

args = parser.parse_args()
npep = args.npep
nwater = args.nwater
mpep = 2884.42
mwater = 18

conc = (npep * mpep) / (npep * mpep + nwater * mwater)
print "npep: {0}, nwater {1}".format(npep, nwater)
print "mpep: {0}, mwater {1}".format(mpep, mwater)
print conc
