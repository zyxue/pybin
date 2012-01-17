#! /usr/bin/env python

import os
from configobj import ConfigObj

from g_analyze import init2 as gai
from g_analyze import organize as gao

VERSION = '2.0'
AUTHOR = 'zyxue'
EMAIL = 'zhuyi.xue@utoronto.ca'

def parse_conf():
    pass

def parse_option():
    pass

def gen_inputargs():
    """loop throught all the directories and gen input args for each"""
    pass

def dirchy(SEQS, CDTS, TMPS, NUMS, config_dict):
    """ generate the directory hierarchy"""
    dirchy_dict = config_dict['dirchy']
    pwd = os.getenv('PWD')
    for seq in SEQS:
        for cdt in CDTS:
            for tmp in TMPS:
                for num in NUMS:
                    tropoinputdir = os.path.join(
                        dirchy_dict['dirchy_d1'],
                        dirchy_dict['dirchy_d2'],
                        dirchy_dict['dirchy_d3'],
                        dirchy_dict['dirchy_d4']
                        )
                    inputdir = tropoinputdir.format(seq=seq, tmp=tmp, cdt=cdt, num=num)
                    # all the following filenames will be named after pf
                    # i.e.  xtcf, proxtcf, tprf, edrf, grof, ndxf
                    pf = dirchy_dict['prefix'].format(seq=seq, tmp=tmp, cdt=cdt, num=num) 
                    if os.path.exists(inputdir):
                        yield inputdir, pf, seq, cdt, tmp, num

def init_dirs(g_tool_name, ARGS, CONFIG_DICT):
    """
    initialize directories like outputdir, and outputdir/LOGS and
    outputdir/LOGS/{g_tool_name_log} if ARGS.nolog is False
    """
    # Get the path for outpudir, if not specified either in your console or in
    # the configuration file, 'R_OUTPUT" will be created in the current
    # directory to avoid scinet crash.
    if ARGS.outputdir:
        outputdir = ARGS.outputdir
    elif CONFIG_DICT.has_key('outputdir'):
        outputdir = CONFIG_DICT['outputdir']
    else:
        outputdir = 'R_OUTPUT'

    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    # parent_logd holds all the logs which will keep the output of the
    # analysis tools you use
    parent_logd = os.path.join(outputdir, 'LOGS') 
    if not os.path.exists(parent_logd) and not ARGS.test: # if your testing, no point to mkdir
        os.mkdir(parent_logd)
                           
    if ARGS.nolog:
        logd = None
    else:
        logd = os.path.join(
            outputdir, 'LOGS', '{0}_log'.format(g_tool_name))

        if not os.path.exists(logd):
            os.mkdir(logd)
    
    return outputdir, logd

def init_seqs_cdts_tmps_nums(args, config_dict):
    seqs = args.SEQS if args.SEQS else config_dict['SEQS']
    cdts = args.CDTS if args.CDTS else config_dict['CDTS']
    tmps = args.TMPS if args.TMPS else config_dict['TMPS']
    nums = args.NUMS if args.NUMS else config_dict['NUMS']
    print seqs, cdts, tmps, nums
    return seqs, cdts, tmps, nums

def gen_input_args(g_tool, g_tool_name, ARGS, CONFIG_DICT):
    """
    generate input_args, which in a dictionary that holds all the varaibles
    needed for your commands
    """
    outputdir, logd = init_dirs(g_tool_name, ARGS, CONFIG_DICT)

    SEQS, CDTS, TMPS, NUMS = init_seqs_cdts_tmps_nums(ARGS, CONFIG_DICT)

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
    non_organize_modules = ['g_analyze.basic', 'g_analyze.interaction']

    for inputdir, pf, seq, cdt, tmp, num in dirchy(SEQS, CDTS, TMPS, NUMS, CONFIG_DICT):
        input_args = dict(inputdir=inputdir, pf=pf, seq=seq, cdt=cdt, num=num)

        # gen paths for input files: xtcf, proxtcf, tprf, edrf, grof, ndxf
        input_args.update(gai.gen_input_files(
                inputdir, input_args['pf']))

        # gen outputdir, etc. if any output files are produced
        if g_tool.__module__ in non_organize_modules: # if in organize module, no new dir needs to be created
            anadir = os.path.join(outputdir, 'r_' + g_tool_name) # anadir should be a subfolder under outputdir
            input_args['anadir'] = anadir
            if not os.path.exists(anadir) and not ARGS.test:
                os.mkdir(anadir)
        
        # this part will be improved later, particular when using a database
        if ARGS.cdb:
            import connect_db as cdb
            ss = cdb.connect_db(CONFIG_DICT['database'])
            query = ss.query(cdb.Cutoff_rg_alltrj).filter_by(sqid=seq)
            time_for_b = query.value(cdt)
            input_args['b'] = time_for_b
        else:
            input_args['b'] = 0                                       # default

        # particular to make_ndx
        if ARGS.toa == 'g_make_ndx':
            ndx_id = CONFIG_DICT['ndx_input']                  # ndx_input_dict
            ndx_fd = CONFIG_DICT['ndx_format']                 # ndx_format_dict
            from pprint import pprint as pp
            # pp(locals())
            input_args['ndx_input'] = ' '.join([ndx_id[ndx_fd[f].format(**locals())] for f in ndx_fd])

        if ARGS.toa == 'sequence_spacing':
            from Mysys import read_mysys_dat
            mysys = read_mysys_dat()
            input_args['peptide_length'] = mysys[seq].len

        if ARGS.btime:
            input_args['b'] = ARGS.btime

        cmd = g_tool(input_args)
        if logd:
            logf = os.path.join(logd, '{0}.log'.format(input_args['pf']))
        else:                                             # meaning logd is None
            logf = None

        yield (cmd, logf)

def main():
    # determine which function to call
    g_tool, ARGS = gai.target_the_type_of_analysis()
    g_tool_name =  g_tool.func_name

    config_file = ARGS.config_file
    if not os.path.exists(config_file):
        raise ValueError('configuration file: {0} may not exist!'.format(config_file))
    config_dict = ConfigObj(config_file)

    x = gen_input_args(g_tool, g_tool_name, ARGS, config_dict)
    # gai.runit(x, ARGS.numthread)

    print "#" * 20
    from pprint import pprint as pp
    pp(ARGS)
    print "#" * 20

if __name__ == "__main__":
    main()

