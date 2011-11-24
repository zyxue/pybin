#!/usr/bin/env python

"""

This module includes functions that are required for initiation, by which I mean
overhead for starting analysis

"""

import os
import glob
import subprocess
import Queue
from optparse import OptionParser
from threading import Thread

import organize
import basic

AVAILABLE_ANALYSIS = organize.__all__ + basic.__all__

def gen_input_files(target_dir, pf):
    """
    Generalizing input files specific for gromacs tools
    """

    input_files = dict(
        xtcf = os.path.join(target_dir, '{pf}_md.xtc'.format(pf=pf)),
        proxtcf = os.path.join(target_dir, '{pf}_pro.xtc'.format(pf=pf)),
        tprf = os.path.join(target_dir, '{pf}_md.tpr'.format(pf=pf)),
        edrf = os.path.join(target_dir, '{pf}_md.edr'.format(pf=pf)),
        grof = os.path.join(target_dir, '{pf}_md.gro'.format(pf=pf)),
        ndxf = os.path.join(target_dir, '{pf}.ndx'.format(pf=pf)))

    hb_tprf = os.path.join(target_dir, '{pf}_md_hbond.tpr'.format(pf=pf)) # potentially needed
    if os.path.isfile(hb_tprf):
        input_files.update(dict(hb_tprf=hb_tprf))
    return input_files

def runit(cmd_logf_generator):
    """
    Putting each analyzing codes in a queue to use the 8 cores simutaneously.
    """
    def worker():
        while True:
            cmd, logf = q.get()
            if OPTIONS.test:
                print cmd
            else:
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

    for i in range(16):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for cmd_logf in cmd_logf_generator:
        q.put(cmd_logf)
    
    q.join()

def convert_seq_or_cdt_or_num(option, opt_str, value, parser):
    if opt_str in ['-c', '--cdt']:
        parser.values.CDTS = value.split()
    elif opt_str in ['-s', '--seq', '-n', '--num']:
        if '-' in value:                   # process args like "-s 1-9"
            mi, ma = [int(i) for i in value.split('-')]
            range_ =  range(mi, ma + 1)
        else:
            range_ =  [int(i) for i in value.split()]
        if opt_str in ['-s', '--seq']:
            parser.values.SEQS = [ 'sq' + str(i) for i in range_]
        elif opt_str in ['-n', '--num']:
            parser.values.NUMS = [ '{0:02d}'.format(i) for i in range_]

def parse_cmd():
    """parse_cmd"""
    parser = OptionParser(usage='loop_dir.py -s "sq[1-2]" -c "[mw]" -n "[01][0-9]" -a="check_target_dirs"')
    parser.add_option('-s', '--seq', type='str', dest='SEQS', default=None, action='callback', callback=convert_seq_or_cdt_or_num,
                      help='specify it this way, i.e. "1 3 4" or "1-9"'  )
    parser.add_option('-c', '--cdt', type='str', dest='CDTS', default=None, action='callback', callback=convert_seq_or_cdt_or_num,
                      help='specify it this way, i.e. "w m o p e"')
    parser.add_option('-n', '--num', type='str', dest='NUMS', default=None, action='callback', callback=convert_seq_or_cdt_or_num,
                      help='specify the replica number, i.e. "1 2 3" or "1-20"')
    parser.add_option('-a','--type_of_analysis', type='str', dest='toa', default=None,
                      help='available_options:\n%r' % AVAILABLE_ANALYSIS )
    parser.add_option('--test', dest='test', action='store_true', default=False)
    parser.add_option('--nolog', dest='nolog', action='store_true', default=False)

    global OPTIONS
    (OPTIONS, args) = parser.parse_args()
    return OPTIONS

def target_the_type_of_analysis():
    OPTIONS = parse_cmd()
    if OPTIONS.toa == "check_inputdirs":
        g_tool = organize.check_inputdirs
        g_tool_name = organize.check_inputdirs.func_name
    elif OPTIONS.toa == "g_trjcat":
        g_tool = organize.g_trjcat
        g_tool_name = organize.g_trjcat.func_name
    elif OPTIONS.toa == "g_eneconv":
        g_tool = organize.g_eneconv
        g_tool_name = organize.g_eneconv.func_name
    elif OPTIONS.toa == "g_trjconv_pro_xtc":
        g_tool = organize.g_trjconv_pro_xtc
        g_tool_name = organize.g_trjconv_pro_xtc.func_name
    elif OPTIONS.toa == "g_trjconv_gro":
        g_tool = organize.g_trjconv_gro
        g_tool_name = organize.g_trjconv_gro.func_name
    elif OPTIONS.toa == "g_trjconv_pro_gro":
        g_tool = organize.g_trjconv_pro_gro
        g_tool_name = organize.g_trjconv_pro_gro.func_name
    elif OPTIONS.toa == "g_make_ndx":
        g_tool = organize.g_make_ndx
        g_tool_name = organize.g_make_ndx.func_name
    elif OPTIONS.toa == 'rg_alltrj':
        g_tool = basic.rg_alltrj
        g_tool_name = basic.rg_alltrj.func_name
    elif OPTIONS.toa == 'rg_backbone':
        g_tool = basic.rg_backbone
        g_tool_name = basic.rg_backbone.func_name
    elif OPTIONS.toa == 'e2ed':
        g_tool = basic.e2ed
        g_tool_name = basic.e2ed.func_name
    else:
        g_tool = 'NO_G_TOOL'
        g_tool_name = 'NO_G_TOOL_NAME'
    return g_tool, g_tool_name, OPTIONS
