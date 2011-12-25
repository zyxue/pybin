#! /usr/bin/env python

import os
from configobj import ConfigObj

from g_analyze import init as gai
from g_analyze import organize as gao

def dirchy(SEQS, CDTS, TMPS, NUMS, CONFIG_DICT):
    """ generate the directory hierarchy"""
    dirchy_dict = CONFIG_DICT['dirchy']
    pwd = os.getenv('PWD')
    for seq in SEQS:
        for cdt in CDTS:
            for tmp in TMPS:
                for num in NUMS:
                    d1 = dirchy_dict['dirchy_d1'].format(seq=seq, tmp=tmp, cdt=cdt, num=num)
                    d2 = dirchy_dict['dirchy_d2'].format(seq=seq, tmp=tmp, cdt=cdt, num=num)
                    d3 = dirchy_dict['dirchy_d3'].format(seq=seq, tmp=tmp, cdt=cdt, num=num)
                    d4 = dirchy_dict['dirchy_d4'].format(seq=seq, tmp=tmp, cdt=cdt, num=num)
                    # all the following filenames will be named after pf
                    pf = dirchy_dict['prefix'].format(seq=seq, tmp=tmp, cdt=cdt, num=num) 
                    # where holds the xtcf, proxtcf, tprf, edrf, grof, ndxf
                    inputdir = os.path.join(pwd, d1, d2, d3, d4)
                    if os.path.exists(inputdir):
                        yield inputdir, pf, seq, cdt, tmp, num

def init_dirs(g_tool_name, OPTIONS, CONFIG_DICT):
    """
    initialize directories like outputdir, and outputdir/LOGS and
    outputdir/LOGS/{g_tool_name_log} if OPTIONS.nolog is False
    """

    # Get the path for outpudir, if not specified either in your console or in
    # the configuration file, 'R_OUTPUT" will be created in the current
    # directory to avoid scinet creash.
    if OPTIONS.outputdir:
        outputdir = OPTIONS.outputdir
    elif CONFIG_DICT.has_key('outputdir'):
        outputdir = CONFIG_DICT['outputdir']
    else:
        outputdir = 'R_OUTPUT'

    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    # parent_logd holds all the logs which will keep the output of the
    # analysis tools you use
    parent_logd = os.path.join(outputdir, 'LOGS') 
    if not os.path.exists(parent_logd) and not OPTIONS.test: # if your testing, no point to mkdir
        os.mkdir(parent_logd)
                           
    if OPTIONS.nolog:
        logd = None
    else:
        logd = os.path.join(
            outputdir, 'LOGS', '{0}_log'.format(g_tool_name))

        if not os.path.exists(logd):
            os.mkdir(logd)
    
    return outputdir, logd

def init_seqs_cdts_tmps_nums(options, config_dict):
    seqs = options.SEQS if options.SEQS else config_dict['SEQS']
    cdts = options.CDTS if options.CDTS else config_dict['CDTS']
    tmps = options.TMPS if options.TMPS else config_dict['TMPS']
    nums = options.NUMS if options.NUMS else config_dict['NUMS']
    print seqs, cdts, tmps, nums
    return seqs, cdts, tmps, nums

def gen_input_args(g_tool, g_tool_name, OPTIONS, CONFIG_DICT):
    """
    generate input_args, which in a dictionary that holds all the varaibles
    needed for your commands
    """
    outputdir, logd = init_dirs(g_tool_name, OPTIONS, CONFIG_DICT)

    SEQS, CDTS, TMPS, NUMS = init_seqs_cdts_tmps_nums(OPTIONS, CONFIG_DICT)

    # if any of SEQS, CDTS, TMPS, NUMS is None, read from .g_ana.cfg
    if not SEQS:
        SEQS = config_dict['SEQS'] 

    if not CDTS:
        CDTS = config_dict['CDTS']

    if not TMPS:
        TMPS = config_dict['TMPS']

    if not NUMS:
        NUMS = config_dict['NUMS']

    # more will be appended in the future
    non_organize_modules = ['g_analyze.basic']

    for inputdir, pf, seq, cdt, tmp, num in dirchy(SEQS, CDTS, TMPS, NUMS, CONFIG_DICT):
        input_args = dict(inputdir=inputdir, pf=pf, seq=seq, cdt=cdt, num=num)

        # gen paths for input files: xtcf, proxtcf, tprf, edrf, grof, ndxf
        input_args.update(gai.gen_input_files(
                inputdir, input_args['pf']))

        # gen outputdir, etc. if any output files are produced
        if g_tool.__module__ in non_organize_modules: # if in organize module, no new dir needs to be created
            anadir = os.path.join(outputdir, 'r_' + g_tool_name) # anadir should be a subfolder under outputdir
            input_args['anadir'] = anadir
            if not os.path.exists(anadir) and not OPTIONS.test:
                os.mkdir(anadir)
        
        # this part will be improved later, particular when using a database
        if OPTIONS.cdb:
            import connect_db as cdb
            ss = cdb.connect_db(CONFIG_DICT['database'])
            query = ss.query(cdb.Cutoff_rg_alltrj).filter_by(sqid=seq)
            time_for_b = query.value(cdt)
            input_args['b'] = time_for_b
        else:
            input_args['b'] = 0                                       # default

        # particular to make_ndx
        if OPTIONS.toa == 'g_make_ndx':
            ndx_id = CONFIG_DICT['ndx_input']                  # ndx_input_dict
            ndx_fd = CONFIG_DICT['ndx_format']                 # ndx_format_dict
            from pprint import pprint as pp
            # pp(locals())
            input_args['ndx_input'] = ' '.join([ndx_id[ndx_fd[f].format(**locals())] for f in ndx_fd])

        if OPTIONS.toa == 'sequence_spacing':
            from Mysys import read_mysys_dat
            mysys = read_mysys_dat()
            input_args['peptide_length'] = mysys[seq].len

        if OPTIONS.btime:
            input_args['b'] = OPTIONS.btime

        cmd = g_tool(input_args)
        if logd:
            logf = os.path.join(logd, '{0}.log'.format(input_args['pf']))
        else:                                             # meaning logd is None
            logf = None

        yield (cmd, logf)

if __name__ == "__main__":
    # determine which function to call
    g_tool, g_tool_name, OPTIONS = gai.target_the_type_of_analysis()

    config_file = OPTIONS.config_file
    CONFIG_DICT = ConfigObj(config_file)

    x = gen_input_args(g_tool, g_tool_name, OPTIONS, CONFIG_DICT)
    gai.runit(x, OPTIONS.numthread)

    print "#" * 20
    from pprint import pprint as pp
    pp(OPTIONS)
    print "#" * 20

#!/env/bin/env python

"""

DIFFERENCE BETWEEN organization & basic MODULE:

analysis in basic module will have output written to anadir

REMEMBER:

##########
When you add a new function, add the function name to __all__, too.
##########

"""

__all__ = ['g_energy_tmpr', 'rg', 'rg_backbone', 'rg_c_alpha', 'e2ed',
           'sequence_spacing', 'do_dssp_E']

def g_energy_tmpr(kwargs):
    return 'printf "14" | g_energy -f {edrf} -o {anadir}/{pf}_tmpr_md.xvg'.format(**kwargs)

def rg(kwargs):
    return 'printf "Protein" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -o {anadir}/{pf}_rg.xvg'.format(**kwargs)

def rg_backbone(kwargs):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return 'printf "Backbone" | g_gyrate -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_rg_backbone.xvg'.format(**kwargs)

def rg_c_alpha(kwargs):
    """
    Radius of Gyration: backbone heavy atoms only. e.g. for (GVPGV)7, there would be 107 atoms,
    which is 35 * 3 + 2 (modified ends)
    """
    return "printf 'C-alpha' | g_gyrate -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_rg_c_alpha.xvg".format(**kwargs)

def e2ed(kwargs):
    """end to end distance"""
    return 'printf "ACE_&_CH3\nNH2_&_N" | myg_dist -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -o {anadir}/{pf}_e2ed.xvg'.format(**kwargs)

def sequence_spacing(kwargs):
    """2011-11-30: sequence_spacing.py, Andreas Vitalis, Xiaoling Wang and Rohi V.Pappu 2008 JMB"""
    return "sequence_spacing.py --pf {pf} -f {xtcf} -s {grof} -l {peptide_length} --atom-sel \'resid {{0}} and not type H\' -o {anadir}/{pf}_sequence_spacing.xvg".format(**kwargs)

def do_dssp_E(kwargs):
    return 'printf "Protein" | do_dssp -f {xtcf} -s {tprf} -sss E -b {b} -sc {anadir}/{pf}_dssp_E.xvg -o {anadir}/{pf}_dssp_E.xpm'.format(**kwargs)
outputdir = '/scratch/p/pomes/zyxue/mono_vac/v700_su/r_ana_results'
database = '/scratch/p/pomes/zyxue/mono_su_as/mono_su_as.db'

[dirchy]
    dirchy_d1 = '{seq}v700'
    dirchy_d2 = '{seq}v700s{num}'
    dirchy_d3 = ''		  # empty dirchy_dx should not be be removed since loop_dir.py will still use it
    dirchy_d4 = ''		  # I think 4 level is enough for now 2011-11-29
    prefix = '{seq}v700s{num}'

[ndx_format]
    # will all be added up in order
    ndxf1 = 'ndx_{seq}'
    ndxf2 = 'ndx_end1'
    ndxf3 = 'ndx_end2'
    ndxf4 = 'ndx_q'			     # the last one will always be ndx_q

[ndx_input]
    # Up: backbone, N, O, and (OE1 & NE2 if GLN exists)
    # Un: CG1 & CG2 for VAL, CB & CG & CD for PRO, CB for ALA, CA for GLY, CB & CD for GLN
    # Vp: O, C[1-8] for o
    # Vn: C for meo, eth, pro
    
    # 1 [ Protein ], 9 [SideChain-H] default 13 groups	
    
    # (GVPGV)7 ENDs not included, CB of VAL not included. Useless groups have to be deleted separately due to gromacs set.
    ndx_sq1 = '1 & !r ACE NH2 & a O N\n r GLY & a CA\n r VAL & a CG1 CG2\n r PRO & a CB CG CD\n 15|16|17\n del 15\n del 15\n del 15\n'
    # (GGVGV)7
    ndx_sq2 = '1 & !r ACE NH2 & a O N\n r GLY & a CA\n r VAL & a CG1 CG2\n 15|16\n del 15\n del 15\n'
    # (PGV)7
    ndx_sq3 = '1 & !r ACE NH2 & a O N\n r GLY & a CA\n r VAL & a CG1 CG2\n r PRO & a CB CG CD\n 15|16|17\n del 15\n del 15\n del 15\n'
    # (GVGVA)7
    ndx_sq4 = '1 & !r ACE NH2 & a O N\n r GLY & a CA\n r VAL & a CG1 CG2\n r ALA & a CB\n 15|16|17\n del 15\n del 15\n del 15\n'
    # (G)35 # in order to be consistent
    ndx_sq5 = '1 & !r ACE NH2 & a O N\n r GLY & a CA\n'
    # (GV)18
    ndx_sq6 = '1 & !r ACE NH2 & a O N\n r GLY & a CA\n r VAL & a CG1 CG2\n 15|16\n del 15\n del 15\n'
    # (Q)35
    ndx_sq7 = '1 & !r ACE NH2 & a O N OE1 NE2\n r GLN & a CB CG\n'
    # (A)35
    ndx_sq8 = '1 & !r ACE NH2 & a O N\n r ALA & a CB\n'
    # (P)35
    ndx_sq9 = '1 & !r ACE NH2 & a O N\n r PRO & a CB CG CD\n'
    
    ndx_end1 = 'r ACE & a CH3\n'
    ndx_end2 = 'r NH2 & a N  \n'					      # used to calculate end2end distance

    ndx_q = 'q\n'

# FYI:
 #  0 System              :   429 atoms
 #  1 Protein             :   429 atoms
 #  2 Protein-H           :   207 atoms
 #  3 C-alpha             :    35 atoms
 #  4 Backbone            :   107 atoms
 #  5 MainChain           :   143 atoms
 #  6 MainChain+Cb        :   164 atoms
 #  7 MainChain+H         :   173 atoms
 #  8 SideChain           :   256 atoms
 #  9 SideChain-H         :    64 atoms
 # 10 ACE_&_CH3           :     1 atoms
 # 11 NH2_&_N             :     1 atoms

"""

This is the g_analyze module

Cannot find the modules in this directory when 

>>>import g_analyze
>>>g_analyze.basic                                                    # doesn't work!!!


"""


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
        'do_dssp_E': [basic.do_dssp_E,
                      basic.do_dssp_E.func_name]
        }
    if options.toa in analysis_methods:
        g_tool, g_tool_name = analysis_methods[options.toa]
    else:
        raise ValueError('You must specify -a option, \n to see what command is gonna be parsed, use --test')
    return g_tool, g_tool_name, OPTIONS
#!/usr/bin/env python

"""

This file includes files that are relevant to analyzing different types of
interaction.

NOTE: PROBABLY THIS FILE WILL BE REWRITTEN!!! 2011-11-18

"""

__all__ = ['unun', 'unvn', 'unvp', 'upun', 'upup', 'upvn', 'upvp', 'vnvn', 'vpvn', 'vpvp']

def inter_groups_matrix():
    igm = {
        'upup':'"16\n16"','upun':'"16\n17"','unun':'"17\n17"',
        'upvp':'"16\n14"','upvn':'"16\n15"','unvp':'"17\n14"','unvn':'"17\n15"',
        'vpvp':'"14\n14"','vpvn':'"14\n15"','vnvn':'"15\n15'
        }                                                # interaction matrix groups
    return igm

def inter_cutoffs():
    ic = {
        'upup':0.35,'upun':0.44,'unun':0.53,
        'upvp':0.35,'upvn':0.44,'unvp':0.44,'unvn':0.53,
        'vpvp':0.35,'vpvn':0.44,'vnvn':0.53
        }
    return ic

hb_template = '-s {tprf} -b {b} -r {icff:.2f} -nonitacc -num {anadir}/{pf}_{g_tool}.xvg'

uu_hb_template = 'printf "1\n1" | g_hbond -f {{proxtcf}} {hb_template}'.format(hb_template=hb_template)
uv_hb_template = 'printf "1\n12" | g_hbond -f {{xtcf}} {hb_template}'.format(hb_template=hb_template)
vv_hb_template = 'printf "12\n12" | g_hbond -f {{xtcf}} {hb_template}'.format(hb_template=hb_template)

uu_nonhb_template = 'printf {igrp} | g_mindist_excl1 -f {proxtcf} -s {tprf} -n {ndxf} -b {b} -d {icff:.2f} -on {anadir}/{pf}_{g_tool}.xvg -od {anadir}/tmp_{pf}.xvg'
ux_nonhb_template = 'printf {igrp} | g_mindist_excl1 -f {xtcf}    -s {tprf} -n {ndxf} -b {b} -d {icff:.2f} -on {anadir}/{pf}_{g_tool}.xvg -od {anadir}/tmp_{pf}.xvg'

"""THE FOLLOWING FUNCTIONS HAVE TO BE SEPARATED BECAUSE THEIR RETURN VALUES
CONTAIN THE __NAME__ OF THE FUNCTION"""

####################UUI####################
def upup(kwargs): # dDA < 3.5nm & angle ADH<30 degree, which is the default criteria in gromacs 4.0.7
    if kwargs.has_key('hb_tprf'):
        kwargs['tprf'] = kwargs['hb_tprf']
    return uu_hb_template.format(**kwargs)

def upun(kwargs):
    return uu_nonhb_template.format(**kwargs)

def unun(kwargs):
    return uu_nonhb_template.format(**kwargs)

####################UVI####################
def upvp(kwargs):
    if kwargs.has_key('hb_tprf'):
        kwargs['tprf'] = kwargs['hb_tprf']
    return uv_hb_template.format(**kwargs)

def upvn(kwargs):
    return 'echo' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)

def unvp(kwargs):
    return ux_nonhb_template.format(**kwargs)

def unvn(kwargs):
    return 'echo' if kwargs['cdt'] == 'w' else ux_nonhb_template .format(**kwargs) 

####################VVI####################
def vpvp(kwargs):
    return vv_hb_template.format(**kwargs)

def vpvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)

def vnvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_nonhb_template.format(**kwargs)
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
#!/scinet/gpc/tools/Python/Python262/bin/python

####################RDF Calculation####################

__all__ = ['rdf_unun', 'rdf_unvn', 'rdf_unvp', 'rdf_upun', 'rdf_upup',
           'rdf_upvn', 'rdf_upvp', 'rdf_vnvn', 'rdf_vpvn', 'rdf_vpvp']

uu_rdf_template = 'printf {inter_groups} | g_rdf_excl1 -f {proxtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {outputdir}/{pf}_{g_tool}.xvg' # rdf within solutes
ux_rdf_template = 'printf {inter_groups} | g_rdf -f {xtcf} -s {tprf} -b {b} -n {ndxf} -bin 0.02 -o {outputdir}/{pf}_{g_tool}.xvg' # rdf between different molecules

def rdf_upup(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_upun(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_unun(kwargs):
    return uu_rdf_template.format(**kwargs)

def rdf_upvp(kwargs):
    return ux_rdf_template.format(**kwargs)

def rdf_upvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)

def rdf_unvp(kwargs):
    return ux_rdf_template.format(**kwargs)

def rdf_unvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)

def rdf_vpvp(kwargs):
    return ux_rdf_template.format(**kwargs)

def rdf_vpvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)

def rdf_vnvn(kwargs):
    return 'pwd' if kwargs['cdt'] == 'w' else ux_rdf_template.format(**kwargs)


