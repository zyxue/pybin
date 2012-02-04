#!/usr/bin/env python

"""

This module includes functions that are required for initiation, by which I mean
overhead for starting analysis

"""

import os
import sys
import glob
import subprocess
import Queue
import logging
import argparse
from threading import Thread

import organize
import interaction
import basic
import rdf

from argparse_action import convert_seq, convert_num

AVAILABLE_ANALYSIS = organize.__all__ + basic.__all__ + interaction.__all__ + rdf.__all__

ANALYSIS_METHODS = {                                    # this dict will keep increasing
    'check_inputdirs': organize.check_inputdirs,
    "g_trjcat": organize.g_trjcat,
    "g_eneconv": organize.g_eneconv,
    "g_trjconv_pro_xtc": organize.g_trjconv_pro_xtc,
    "g_trjconv_gro": organize.g_trjconv_gro,
    "g_trjconv_pro_gro": organize.g_trjconv_pro_gro,
    "g_make_ndx": organize.g_make_ndx,
    "copy_0_mdrun_sh": organize.copy_0_mdrun_sh,
    'rg': basic.rg,
    'rg_backbone': basic.rg_backbone,
    'rg_c_alpha': basic.rg_c_alpha,
    'e2ed': basic.e2ed,
    # 'e2ed_v': basic.e2ed_v,
    'sequence_spacing': basic.sequence_spacing,
    'dssp_E': basic.dssp_E,

    'upup60': interaction.upup60,

    'unun': interaction.unun,

    'upvp': interaction.upvp,
    'upvn': interaction.upvn,
    'unvp': interaction.unvp,
    'unvn': interaction.unvn,

    'rdf_upvp': rdf.rdf_upvp,
    'rdf_upvn': rdf.rdf_upvn,
    'rdf_unvp': rdf.rdf_unvp,
    'rdf_unvn': rdf.rdf_unvn,
    }

def runit(cmd_logf_generator, numthread, ftest):
    """
    Putting each analyzing codes in a queue to use the 8 cores simutaneously.
    """
    def worker():
        while True:
            cmd, logf = q.get()
            if ftest:
                print cmd
            else:
                logging.info('working on {0:s}'.format(cmd))
                if logf is None:
                    p = subprocess.call(cmd, shell=True)
                else:
                    with open(logf, 'w') as opf:
                        p = subprocess.Popen(cmd, shell=True, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE)
                        for data in p.communicate():
                            opf.writelines(data)          # both stdout & stderr
                        opf.write(
                            "{0:s} # returncode: {1:d}\n".format(
                                cmd, p.returncode))
            q.task_done()

    q = Queue.Queue()

    for i in range(numthread):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for cmd_logf in cmd_logf_generator:
        q.put(cmd_logf)
    
    q.join()

def parse_cmd():
    """parse_cmd"""
    parser = argparse.ArgumentParser(usage="-s, -c, -t, -n (don't use quotes)")

    parser.add_argument('-s', dest='SEQS', nargs='+', action=convert_seq,
                        help="specify it this way, i.e. 1 3 4 or 1-9 (don't include 'sq')")
    parser.add_argument('-c', dest='CDTS', nargs='+',
                        help="specify it this way, i.e. w m o p e ")
    parser.add_argument('-t', dest='TMPS', default=None, nargs='+',
                        help='specify it this way, i.e "300 700", maybe improved later')
    parser.add_argument('-n', dest='NUMS', nargs='+', action=convert_num, required=True,
                        help='specify the replica number, i.e. 1 2 3 or 1-20')
    parser.add_argument('--nt', type=int, dest='numthread', default=16,
                        help='specify the number of threads, default is 16')
    parser.add_argument('-a','--type_of_analysis', type=str, dest='toa', required=True,
                        help='available_options:\n{0!r}'.format(AVAILABLE_ANALYSIS))
    parser.add_argument('-b', type=int, dest='btime', default=0,
                        help='specify the beginning time, corresponding to the -b option in gromacs (ps)')
    parser.add_argument('--config_file', type=str, dest='config_file', default='./.g_ana.conf',
                        help='specify the configuration file, default as ./g_ana.conf')
    parser.add_argument('--outputdir', type=str, dest='outputdir', default=None,
                        help='specify the output directory, which will overwrite that in .g_ana.conf')
    parser.add_argument('--test', dest='test', action='store_true', default=False, 
                        help='for debugging, commands will be printed rather than executed')
    parser.add_argument('--nolog', dest='nolog', action='store_true', default=False,
                        help='stdout will be printed to the screen rather than collected in a log file')
    parser.add_argument('--cdb', dest='cdb', action='store_true', default=False,
                        help=''.join(['if you need different b values for different trjectory,', 
                                     'and they are stored in a database specified in your .g_ana.conf']))
    args = parser.parse_args()
    return args

def target_the_type_of_analysis():
    args = parse_cmd()
    if args.toa in ANALYSIS_METHODS:
        g_tool = ANALYSIS_METHODS[args.toa]
    else:
        raise ValueError('You must specify -a option, \n to see what command is gonna be executed, use --test')
    return g_tool, args

if __name__ == "__main__":
    # g_tool, args = target_the_type_of_analysis()
    # print g_tool, type(g_tool)
    # print g_tool.func_name, type(g_tool.func_name)
    parse_cmd()
