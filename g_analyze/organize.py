#!/usr/bin/env python

import os
import glob
import subprocess
import Queue
from threading import Thread

__all__ = ['check_inputdirs', 'g_eneconv', 'g_make_ndx', 'g_select',
           'g_trjcat', 'g_trjconv_gro', 'g_trjconv_pro_xtc', 'g_trjconv_pro_gro',
           'copy_0_mdrun_sh', 'copy_0_mdrun_py']

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
    cmd = 'trjcat -f {fmt_xtcfs} -o {xtcf}'.format(**input_args)
    return cmd

def g_eneconv(input_args):
    tmpl = '{pf}_md.part[0-9][0-9][0-9][0-9].edr'.format(**input_args)
    edrfs = sorted(glob.glob(os.path.join(input_args['inputdir'], tmpl)))
    input_args.update(dict(fmt_edrfs=' '.join(edrfs)))
    cmd = 'eneconv -f {fmt_edrfs} -o {edrf}'.format(**input_args)
    return cmd

def g_trjconv_gro(input_args):          # used to extract the last frame
    return "echo 'System' | trjconv -f {xtcf} -s {tprf} -pbc whole -b {b} -dump 0 -o {grof}".format(**input_args)

def g_trjconv_pro_xtc(input_args):
    return "echo 'Protein' | trjconv -f {xtcf} -s {tprf} -pbc whole -b {b} -o {proxtcf}".format(**input_args)

def g_trjconv_pro_gro(input_args):
    return "echo '1' | trjconv -f {xtcf} -s {tprf} -pbc whole -b {b} -dump 0 -o {progrof}".format(**input_args)

def g_make_ndx(input_args):
    return "printf '{ndx_input}' | make_ndx -f {grof} -o {ndxf}".format(**input_args)

def g_select(input_args):
    return "g_select -f {grof} -s {tprf} -on {ndxf} -select {g_select_select}".format(**input_args)

def copy_0_mdrun_sh(input_args):
    return "sed -e 's/SEQ/{seq}/g' -e 's/CDT/{cdt}/g' -e 's/NUM/{num}/g' /scratch/p/pomes/zyxue/mono_su_as/repository/smp_0_mdrun.sh > {inputdir}/0_mdrun.sh".format(**input_args)

def copy_0_mdrun_py(input_args):
    return "sed -e 's/_SEQ_/{seq}/g' -e 's/_CDT_/{cdt}/g' -e 's/_NUM_/{num}/g' /mnt/scratch_mp2/pomes/xuezhuyi/mono_su_as/0_mdrun.py > {inputdir}/0_mdrun.py".format(**input_args)

def qsub_0_mdrun_py(input_args):
    return 'pwd=$(pwd); cd {inputdir}; qsub 0_mdrun.py; cd ${{pwd}}'.format(**input_args)
