#!/usr/bin/env python

import os
import subprocess
import argparse

from configobj import ConfigObj
from sumcoreg import generate_hash

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='nodes', default=1, help="numbers of nodes")
args = parser.parse_args()

def main():
    config_dict = ConfigObj(os.path.expanduser('~/pybin/sumcoreg.conf'))
    hostname2clustername = generate_hash(config_dict['HOSTNAMES'])
    thehostname = os.environ['HOSTNAME']
    clustername = hostname2clustername[thehostname]
    if clustername == 'scinet':
        subprocess.call("qsub -l nodes={0}:ppn=8,walltime=02:00:00 -q debug -I".format(args.nodes), shell=True)
    elif clustername == 'mp2':
        subprocess.call("qsub -l nodes={0}:ppn=1,walltime=02:00:00 -q qwork@mp2 -I".format(args.nodes), shell=True)
    elif clustername == 'guillimin':
        subprocess.call("msub -l nodes={0}:ppn=12,walltime=02:00:00 -q debug -I".format(args.nodes), shell=True)

# Available clusternames: scinet, mp2, guillimin, lattice, orca, nestor 


if __name__ == "__main__":
    main()
