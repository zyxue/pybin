#! /usr/bin/env python

import os
SELF_SUBMITTED_FLAG = os.getenv('SELF_SUBMITTED_FLAG', None)

import sys
# sys.path.append("/scratch/p/pomes/zyxue/mono_su_as/trj_makeup/sq1w00_makeup/test_0_mdrun_sh/test_MDRun")

import time
import subprocess
import argparse

import ssh
from configobj import ConfigObj
from MDRun import MDRun

if SELF_SUBMITTED_FLAG:
    # not self submitted" run by the user, not submitted itself
    fexecute = True
else:
    fexecute = False
    parser = argparse.ArgumentParser(usage='0_mdrun.py -s some.tpr -c some.conf [--debug]')
    parser.add_argument('-s', dest='tpr', required=True, type=str,
                        help="tpr file must be specified")
    parser.add_argument('-n', dest='title', type=str, default=None,
                        help="optional title, if not specified, the char before .tpr in tprfile will be used")
    parser.add_argument('-c', dest="conf", required=True, type=str,
                        help="specify the configuration file")
    parser.add_argument('-d', '--debug', dest="debug", action="store_true", default=False,
                        help="specify the configuration file")
    args = parser.parse_args()

    if os.path.exists(args.conf):
        config_dict = ConfigObj(args.conf)
    else:
        raise IOError("{0} cannot found".format(args.conf))
    
    # PREPARE PBS OPTIONS -l
    pbs_kwargs = config_dict['PBS']
    # putting a function here is so ugly
    def get_walltime(x):
        total_seconds = float(x) * 3600
        hh = divmod(total_seconds, 3600)[0]
        mm = divmod(total_seconds - hh * 3600, 60)[0]
        ss = total_seconds - hh * 3600 - mm * 60
        return "{0:02.0f}:{1:02.0f}:{2:02.0f}".format(hh, mm, ss)
    # walltime is determined by maxh to reduce user-controled variable
    maxh = config_dict['MDRUN_MPI']['MAXH']
    pbs_kwargs['WALLTIME'] = get_walltime(maxh) 

    # PREPARE TITLE for -N and -v
    # it's very ugly though
    tpr = os.path.join(os.environ['PWD'], args.tpr)                   # with absolute path
    mdrun = MDRun(tpr)
    if os.path.exists(mdrun.cpt):
        tt = "{0:.0f}".format(mdrun._cpttime(mdrun.cpt) / 1000)       # unit: ns
    else:
        tt = 0
    N = "{0}t{1}".format(args.title if args.title else os.path.basename(tpr)[:-4], tt)

    conf = os.path.join(os.environ['PWD'], args.conf)                   # with absolute path
    cmd = ' '.join(sys.argv)                                          # pass as environ variable

    basic_submit = [
        'qsub', sys.argv[0],
        '-N', N, 
        '-l', 'nodes={NODES}:ppn={PPN},walltime={WALLTIME}'.format(**pbs_kwargs),
        '-m', 'bea',
        '-M', 'alfred532008@gmail.com',
        '-v', 'SELF_SUBMITTED_FLAG=1,TPR={0},CONF={1},CMD="{2}"'.format(tpr, conf, cmd),
        '-q', '{QUEUE}'.format(**pbs_kwargs),
        ]

    if args.debug:
        subprocess.call(basic_submit + ['-q', 'debug'])               # not interactive
    else:
        subprocess.call(basic_submit)

def main():
    tpr = os.environ['TPR']
    conf = os.environ['CONF']
    cmd = os.environ['CMD']
    pbs_o_workdir = os.environ['PBS_O_WORKDIR']

    print time.ctime(), cmd
    print time.ctime(), pbs_o_workdir

    config_dict = ConfigObj(conf)
    host = config_dict['PBS']['HOST']
    mpi_kwargs = config_dict['MDRUN_MPI']

    mdrun = MDRun(tpr, **mpi_kwargs)
    if mdrun.is_finished():
        pass
    else:
        returncode = mdrun.mdrun()
        if returncode == 0:
            s = ssh.Connection(host)
            s.execute('cd {0}; {1}'.format(pbs_o_workdir, cmd))
            s.close()
            print "mdrun successfully at {0}".format(time.ctime())
        else:
            print "mdrun unsuccessfully at {0}".format(time.ctime())

if __name__ == "__main__":
    if fexecute:
        main()
