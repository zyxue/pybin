#!/usr/bin/env python

"""

This module includes functions that are required for initiation, by which I mean
overhead for starting analysis

"""

import os
import glob
import subprocess
import Queue
import logging
from optparse import OptionParser
from threading import Thread

import organize
import interaction
import basic

AVAILABLE_ANALYSIS = organize.__all__ + basic.__all__

def gen_input_files(target_dir, pf):
    """
    Generalizing input files specific for gromacs tools, default naming
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

def runit(cmd_logf_generator, numthread):
    """
    Putting each analyzing codes in a queue to use the 8 cores simutaneously.
    """
    def worker():
        while True:
            cmd, logf = q.get()
            if OPTIONS.test:
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

def convert_seq(option, opt_str, value, parser):
    if not value is None:
        if '-' in value:
            mi, ma = value.split('-')                   # process args like "-s 1-9"
            range_ = [str(i) for i in range(int(mi), int(ma) + 1)]
        else:
            range_ = [i for i in value.split()]
        parser.values.SEQS = [ 'sq' + str(i) for i in range_]

def convert_cdt(option, opt_str, value, parser):
    if not value is None:
        # water, methanol, ethanol, propanol, octane, vacuo
        valid_cdts = ['w', 'm', 'e', 'p', 'o', 'v']
        split_v = value.split()
        for v in split_v:
            if v not in valid_cdts:
                raise ValueError('cdt {0:s} is not one of {1!r}'.format(v, valid_cdts))
        parser.values.CDTS = split_v

def convert_tmp(option, opt_str, value, parser):
    parser.values.TMPS = value.split()

def convert_num(option, opt_str, value, parser):
    if not value is None:
        if '-' in value:                   
            mi, ma = value.split('-')
            range_ = range(int(mi), int(ma) + 1)
        else:
            range_ = [int(i) for i in value.split()]
        parser.values.NUMS = [ '{0:02d}'.format(i) for i in range_]

def parse_cmd():
    """parse_cmd"""
    parser = OptionParser(usage='-s, -c, -t, -n may not function according to your .g_ana.cfg"')
    parser.add_option('-s', '--seq', type='str', dest='SEQS', default=None, action='callback', callback=convert_seq,
                      help='specify it this way, i.e. "1 3 4" or "1-9"; don\'t include \'sq\''  )
    parser.add_option('-c', '--cdt', type='str', dest='CDTS', default=None, action='callback', callback=convert_cdt,
                      help='specify it this way, i.e. "w m o p e"')
    parser.add_option('-t', '--tmp', type='str', dest='TMPS', default=None, action='callback', callback=convert_tmp,
                      help='specify it this way, i.e "300 700", maybe improved later')
    parser.add_option('-n', '--num', type='str', dest='NUMS', default=None, action='callback', callback=convert_num,
                      help='specify the replica number, i.e. "1 2 3" or "1-20"')
    parser.add_option('--nt', type='int', dest='numthread', default=16,
                      help='specify the number of threads')
    parser.add_option('-a','--type_of_analysis', type='str', dest='toa', default=None,
                      help='available_options:\n%r' % AVAILABLE_ANALYSIS )
    parser.add_option('-b', type='int', dest='btime', default=0,
                      help='specify the beginning time, corresponding to the -b option in gromacs')
    parser.add_option('--config_file', type='str', dest='config_file', default='./.g_ana.cfg',
                      help='specify the configuration file')
    parser.add_option('--outputdir', type='str', dest='outputdir', default=None,
                      help='specify the output directory, which will overwrite .g_ana.cfg')
    parser.add_option('--test', dest='test', action='store_true', default=False)
    parser.add_option('--nolog', dest='nolog', action='store_true', default=False)
    parser.add_option('--cdb', dest='cdb', action='store_true', default=False,
                      help='if you need different b values for different trjectory, and they are stored in a database specified in your .g_ana.cfg')

    global OPTIONS
    (OPTIONS, args) = parser.parse_args()
    return OPTIONS

def target_the_type_of_analysis():
    options = parse_cmd()
    analysis_methods = {                                    # this dict will keep increasing
        'check_inputdirs': [organize.check_inputdirs, 
                            organize.check_inputdirs.func_name],
        "g_trjcat" : [organize.g_trjcat,
                      organize.g_trjcat.func_name],
        "g_eneconv": [organize.g_eneconv,
                      organize.g_eneconv.func_name],
        "g_trjconv_pro_xtc": [organize.g_trjconv_pro_xtc,
                              organize.g_trjconv_pro_xtc.func_name],
        "g_trjconv_gro": [organize.g_trjconv_gro,
                          organize.g_trjconv_gro.func_name],
        # "g_trjconv_pro_gro": [organize.g_trjconv_pro_gro,
        #                       organize.g_trjconv_pro_gro.func_name],
        "g_make_ndx": [organize.g_make_ndx,
                       organize.g_make_ndx.func_name],
        "copy_0_mdrun_sh": [organize.copy_0_mdrun_sh,
                            organize.copy_0_mdrun_sh.func_name],
        'rg': [basic.rg,
               basic.rg.func_name],
        'rg_backbone': [basic.rg_backbone,
                        basic.rg_backbone.func_name],
        'rg_c_alpha': [basic.rg_c_alpha,
                          basic.rg_c_alpha.func_name],
        'e2ed': [basic.e2ed,
                 basic.e2ed.func_name],
#         'e2ed_v': [basic.e2ed_v,
#                    basic.e2ed_v.func_name],
        'sequence_spacing': [basic.sequence_spacing,
                             basic.sequence_spacing.func_name],
        'dssp_E': [basic.dssp_E,
                      basic.dssp_E.func_name],
        'upup60': [interaction.upup60,
                   interaction.upup60.func_name]
        }
    if options.toa in analysis_methods:
        g_tool, g_tool_name = analysis_methods[options.toa]
    else:
        raise ValueError('You must specify -a option, \n to see what command is gonna be parsed, use --test')
    return g_tool, g_tool_name, OPTIONS
