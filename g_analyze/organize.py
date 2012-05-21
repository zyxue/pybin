#!/usr/bin/env python

import os
import glob

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

def rename_tpr2old(input_args):
    input_args['tprf_dirname'] = os.path.dirname(input_args['tprf'])
    return 'cp -v {tprf} {tprf_dirname}/{pf}_md.old_200ns.tpr'.format(**input_args)

def generate_500ns_tpr(input_args):                # remember that nstenergy is changed to 1
    input_args['topf'] = os.path.join(os.path.dirname(input_args['tprf']),
                                      'beforenpt',
                                      '{0}.top'.format(input_args['pf']))
    input_args['mdpf'] = os.path.join(os.path.dirname(input_args['tprf']),
                                      '{0}_md.mdp'.format(input_args['pf']))

    return '''grompp -f repository/md_extend_to_500ns.mdp -c {grof} -p {topf} -o {tprf} -po {mdpf}'''.format(**input_args)

def sed_0_mdrun_sh(input_args):
    if '300' in input_args['pf']:
        return 'sed "s/sq1w00/{pf}/g" repository/tmp_0_mdrun.sh > {seq}{cdt}300_su/{seq}{cdt}300s{num}/0_mdrun.sh'.format(**input_args) # mono_meo
    else:
        return 'sed "s/sq1w00/{pf}/g" repository/tmp_0_mdrun.sh > {cdt}300/sq1{cdt}/sq1{cdt}{num}/0_mdrun.sh'.format(**input_args) # mono_su_as

def rename_xtcf_200ns(input_args):
    xtcf = input_args['xtcf']
    xtcf_200ns = xtcf.replace('_md', '_md_200ns')
    if os.path.exists(xtcf):
        return "mv -v {0} {1}".format(xtcf, xtcf_200ns)
    else:
        return "echo ALREADY RENAMED PREVIOUSLY {0} {1}".format(xtcf, xtcf_200ns)

def g_trjcat_500ns(input_args):
    tmpl = '{pf}_md.part[0-9][0-9][0-9][0-9].xtc'.format(**input_args)
    xtcfs = sorted(glob.glob(os.path.join(input_args['inputdir'], tmpl)))
    input_args.update(dict(fmt_xtcfs=' '.join(xtcfs)))

    xtcf = input_args['xtcf']
    input_args.update(dict(xtcf_200ns=xtcf.replace('_md', '_md_200ns')))

    cmd = 'trjcat -f {xtcf_200ns} {fmt_xtcfs} -o {xtcf}'.format(**input_args)
    return cmd

def g_trjconv_centerxtc(input_args):
    # -center -pbc whole : protien is centered, but it's not surrounded by solvent
    # -center -pbc mol   : no tric box anymore, like a cuboid
    # -center -pbc atom  : doesn't correct pbc, not useful
    # -center -pbc mol -ur compact: solvent are ordered closest to the protein
    # -center -pbc mol -ur tric: most suitable in this case
    return "printf 'Protein\nsystem\n' | trjconv -f {xtcf} -s {tprf} -b {b} -center -pbc mol -ur tric -o {centerxtcf}".format(**input_args)
