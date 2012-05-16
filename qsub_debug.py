#!/usr/bin/env python

import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='nodes', default=1, help="numbers of nodes")
args = parser.parse_args()

subprocess.call("qsub -l nodes={0}:ppn=8,walltime=2:00:00 -q debug -I".format(args.nodes), shell=True)
