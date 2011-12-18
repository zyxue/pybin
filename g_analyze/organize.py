#!/usr/bin/env python

import os
import glob
import subprocess
import Queue
from threading import Thread

__all__ = ['check_inputdirs', 'g_eneconv', 'g_make_ndx', 'g_trjcat',
           'g_trjconv_gro', 'g_trjconv_pro_xtc', 'g_trjconv_pro_gro',
           'g_make_ndx', 'copy_0_mdrun_sh']

def check_inputdirs(input_args):
    d = input_args['inputdir']
    if not os.path.exists(d):
        raise ValueError('Check if {0:!s} exists?!'.format(d))
    s = 'echo "{0!s} exists"'.format(d)
    return s

def g_trjcat(input_args):
    tmpl = '{pf}_md.part[0-9][0-9][0-9][0-9].xtc'.format(**input_args)
    xtcfs = sorted(glob.glob(os.path.join(input_args['inputdir'], tmpl)))
    input_args.update(dict(fmt_xtcfs=' '.join(xtcfs)))
    cmd = 'trjcat -f {fmt_xtcfs} -o {inputdir}/{pf}_md.xtc'.format(**input_args)
    return cmd

def g_eneconv(input_args):
    tmpl = '{pf}_md.part[0-9][0-9][0-9][0-9].edr'.format(**input_args)
    edrfs = sorted(glob.glob(os.path.join(input_args['inputdir'], tmpl)))
    input_args.update(dict(fmt_edrfs=' '.join(edrfs)))
    cmd = 'eneconv -f {fmt_edrfs} -o {inputdir}/{pf}_md.edr'.format(**input_args)
    return cmd

def g_trjconv_gro(input_args):          # used to extract the last frame
    return "echo 'System' | trjconv -f {xtcf} -s {tprf} -pbc whole -b {b} -dump 0 -o {inputdir}/{pf}_md.gro".format(**input_args)

def g_trjconv_pro_xtc(input_args):
    return "echo 'Protein' | trjconv -f {xtcf} -s {tprf} -pbc whole -o  {inputdir}/{pf}_pro.xtc".format(**input_args)

# def g_trjconv_pro_gro(input_args):
# USELESS
#     return "echo '1' | trjconv -f {xtcf} -s {tprf} -pbc whole -b {0} -dump 0 -o {inputdir}/{pf}_pro.gro".format(**input_args)

def g_make_ndx(input_args):
    return "printf '{ndx_input}' | make_ndx -f {grof} -o {ndxf}".format(**input_args)

def copy_0_mdrun_sh(input_args):
    return "sed -e 's/SEQ/{seq}/g' -e 's/CDT/{cdt}/g' -e 's/NUM/{num}/g' /scratch/p/pomes/zyxue/mono_su_as/repository/smp_0_mdrun.sh > {inputdir}/0_mdrun.sh".format(**input_args)
