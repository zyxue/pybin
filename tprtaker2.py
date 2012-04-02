#! /usr/bin/env python

import os
import sys
import time
import subprocess
import argparse
import logging

import paramiko
from configobj import ConfigObj

from mdrun import MDRun

"""You could execute this script in any dir, but be noticed that the .[oe] file
will also be written to the dir where you execute this script"""

def main():
    SS_FLAG = os.getenv('SS_FLAG', None)                          # self submission flag
    if SS_FLAG:
        # not self submitted" run by the user, not submitted itself
        exec_mdrun()
    else:
        exec_qsub()

def init_logger(logfile):
    logger = logging.getLogger('tprtaker')
    hdlr = logging.FileHandler(logfile)                        # handler
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    return logger

def zxlog(logger, value, NAME):
    sep = '#### {0:15s} ### {1}'                                         # separator
    logger.info(sep.format(NAME, value))

def exec_mdrun():
    # It is actually in the ${HOME} directory when executing this function,
    # but since MDRun.mdrun doesn't need to cd the PBS_O_WORKDIR, so it's fine
    pbs_o_workdir = os.environ['PBS_O_WORKDIR'] # will be visited after sshed to the host
    logger = init_logger(
        os.path.join(pbs_o_workdir, 'tprtaker.log.{0}'.format(os.environ['PBS_JOBID']))
        )
    zxlog(logger, pbs_o_workdir, 'PBS_O_WORKDIR')

    ss_count = os.environ['SS_COUNT']                  # will be passed when ssh
    zxlog(logger, ss_count, 'SS_COUNT')

    ss_cmd = os.environ['SS_CMD']        # will be executed after sshed to the host
    zxlog(logger, ss_cmd, 'SS_CMD')

    args = parse_cmd(ss_cmd.split()[1:])
    # even if both of tpr & conf are present when first executing tprtake.py,
    # they might have been relocated when the job is queuing
    tpr, conf = check_presence(pbs_o_workdir, args.tpr, args.conf)

    config_dict = ConfigObj(conf)
    ssh_kwargs = config_dict['SSH']
    mpi_kwargs = config_dict['MDRUN_MPI']

    mdrun = MDRun.MDRun(tpr, **mpi_kwargs)
    if mdrun.is_finished():
        pass
    else:
        mdrun_cmd = mdrun.get_mdrun_cmd()
        zxlog(logger, ' '.join(mdrun_cmd), 'MDRUN_CMD') # notice get_mdrun_cmd return a list
        returncode = mdrun.mdrun(mdrun_cmd)       # mdrun_cmd: mdrun commandline
        if returncode == 0:
            zxlog(logger, ' '.join(mdrun_cmd), 'SUCCESSFULLY')
            # NOW SSH
            sshto(ssh_kwargs['conf_hostname'], 
                  ssh_kwargs['conf_username'],
                  cmd='cd {0}; {1}'.format(pbs_o_workdir, ss_cmd))
        else:
            zxlog(logger, ' '.join(mdrun_cmd), 'UNSUCCESSFULLY')

def exec_qsub():
    args = parse_cmd()
    pwd = os.getcwd()

    # START PREPARING THE OPTIONS FOR PBS SUBMISSION

    # just to verify the presences of input files, they don't need to be passed
    # to qsub since the absolute path of those two inputfiles could always be
    # obtained from the command line
    tpr, conf = check_presence(pwd, args.tpr, args.conf)

    # cmd is also passed as environ variable, will be used repeatly (exactly the same
    # command) on following executions
    ss_cmd = ' '.join(sys.argv) 

    ss_count = os.getenv('SS_COUNT')
    if ss_count:
        ss_count = "{0}".format(int(ss_count) + 1)
    else:
        ss_count = 1                                                  # first time self submission

    config_dict = ConfigObj(conf)
    
    # walltime is determined by maxh to reduce user-controled variable
    walltime = calc_walltime(config_dict['MDRUN_MPI']['conf_maxh']) 

    # title could be specified in the command line or derived based on the tpr file
    title = args.title if args.title else make_title(tpr)
    
    pbs_kwargs = config_dict['PBS']
    basic_submit = [
        pbs_kwargs['conf_qsub'], 
        '-v', 'SS_CMD="{0}",SS_FLAG=1,SS_COUNT={1}'.format(ss_cmd, ss_count),
        '-l', pbs_kwargs['conf_l'].format(walltime),
        '-N', title, 
        '-m', pbs_kwargs['conf_m'],
        '-M', pbs_kwargs['conf_M'],
        '-q', pbs_kwargs['conf_q'],
        sys.argv[0],
        ]                                         # SS_ means self submission

    if args.debug:
        print ' '.join(basic_submit)
    else:
        subprocess.call(basic_submit)

def check_presence(dirname, *infiles):
    infs_absp = []                                # infile with absolute path
    for inf in infiles:
        inf_absp = os.path.join(dirname, inf)
        if not os.path.exists(inf_absp):                           
            raise IOError("{0} cannot found".format(inf_absp))
        else:
            infs_absp.append(inf_absp)
    return infs_absp

def calc_walltime(x):
    total_seconds = float(x) * 3600
    hh = divmod(total_seconds, 3600)[0]
    mm = divmod(total_seconds - hh * 3600, 60)[0]
    ss = total_seconds - hh * 3600 - mm * 60
    return "{0:02.0f}:{1:02.0f}:{2:02.0f}".format(hh, mm, ss)

def make_title(tpr):
    mdrun = MDRun.MDRun(tpr)
    if os.path.exists(mdrun.cpt):
        r = subprocess.call(['gmxcheck', '-f', mdrun.cpt], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r != 0:
            tt = "{0:.0f}".format(mdrun._cpttime(mdrun.cpt) / 1000)       # unit: ns
        else:
            tt = "{0:.0f}".format(mdrun._cpttime(mdrun.prev_cpt) / 1000)       # unit: ns
        # Here code is wrong, cpt could have been corrupted, so if possible, it
        # should try to fix it itself
    else:
        tt = 0
    title = "{0}t{1}".format(os.path.basename(tpr)[:-4], tt)
    return title

def sshto(host, username, cmd):
    """cmd should be a string, not list"""
    # check the existence of ~/.ssh/id_rsa (or id_dsa?)
    rsa_key_file = os.path.expanduser('~/.ssh/id_rsa')
    if not os.path.exists(rsa_key_file):
        raise IOError('{0} rsa_key_file cannot found'.format(rsa_key_file))
    rsa_key = paramiko.RSAKey.from_private_key_file(rsa_key_file)
    # input must be a socket-like object
    channel = paramiko.Transport((host, 22)) 
    channel.connect(username=username, pkey=rsa_key)
    session = channel.open_session()
    session.exec_command(cmd)
    channel.close()

def parse_cmd(cmd=None):
    parser = argparse.ArgumentParser(usage='0_mdrun.py -s some.tpr -c some.conf [--debug]')
    parser.add_argument('-s', dest='tpr', type=str, required=True,
                        help="tpr file must be specified")
    parser.add_argument('-c', dest="conf", type=str, required=True, 
                        help="specify the configuration file")
    parser.add_argument('-n', dest='title', type=str, default=None,
                        help="optional title, if not specified, the char before .tpr in tprfile will be used")
    parser.add_argument('-d', '--debug', dest="debug", action="store_true", default=False,
                        help="specify the configuration file")
    if cmd:
        args = parser.parse_args(cmd)
    else:
        args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
