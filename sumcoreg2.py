#! /usr/bin/env python

import os

from configobj import ConfigObj
from JobOverseer import clusters


__version__ = 3

def generate_hash(dd):
    new_dd = {}
    for k in dd:
        for v in dd[k]:
            new_dd[v] = k
    return new_dd

def main():
    config_dict = ConfigObj(os.path.expanduser('~/pybin/sumcoreg.conf'))

    username2realname = generate_hash(config_dict['USERS'])

    hostname2clustername = generate_hash(config_dict['HOSTNAMES'])

    thehostname = os.environ['HOSTNAME']

    clustername = hostname2clustername[thehostname]

    cluster_kwargs = config_dict['CLUSTERS'][clustername]

    cores, statcmd = cluster_kwargs.values()
    
    cluster = clusters.Cluster(clustername, cores, statcmd, username2realname)
    cluster.report_to_me()

if __name__ == "__main__":
    main()
