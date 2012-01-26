#! /usr/bin/env python

import os
from configobj import ConfigObj

from g_analyze import init2 as gai
from g_analyze import organize as gao

VERSION = '2.0'
AUTHOR = 'zyxue'
EMAIL = 'zhuyi.xue@utoronto.ca'

def gen_input_files(target_dir, pf):
    """
    Generalizing input files specific for gromacs tools, default naming
    """

    input_files = dict(
        xtcf = os.path.join(
            target_dir, '{pf}_md.xtc'.format(pf=pf)),
        grof = os.path.join(
            target_dir, '{pf}_md.gro'.format(pf=pf)),
        proxtcf = os.path.join(
            target_dir, '{pf}_pro.xtc'.format(pf=pf)),
        progrof = os.path.join(
            target_dir, '{pf}_pro.gro'.format(pf=pf)),
        tprf = os.path.join(
            target_dir, '{pf}_md.tpr'.format(pf=pf)),
        edrf = os.path.join(
            target_dir, '{pf}_md.edr'.format(pf=pf)),
        ndxf = os.path.join(
            target_dir, '{pf}.ndx'.format(pf=pf)))

    hb_tprf = os.path.join(
        target_dir, '{pf}_md_hbond.tpr'.format(pf=pf)) # potentially needed
    if os.path.isfile(hb_tprf):
        input_files.update(dict(hb_tprf=hb_tprf))
    return input_files

def dirchy(SEQS, CDTS, TMPS, NUMS, dirchy_dict):
    """ generate the directory hierarchy"""
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

def gen_input_args(g_tool, g_tool_name, outputdir, logd, directory_hierarchy,
                   ftest, fcdb, toa, btime):
    """
    generate "input_args", which in a dictionary that holds all the varaibles
    needed for your commands
    """
    for inputdir, pf, seq, cdt, tmp, num in directory_hierarchy:
        input_args = dict(inputdir=inputdir, pf=pf, seq=seq, cdt=cdt, num=num)

        # gen paths for input files:
        # (when organizing, input files could also be outputfiles)
        # xtcf, grof, proxtcf, progrof, tprf, edrf, ndxf
        input_args.update(gen_input_files(inputdir, pf))

        # if g_tool is from organize module, no new dir needs to be created
        # to compare string, is doesn't work (confirmed)
        if not g_tool.__module__ == 'g_analyze.organize':
            # anadir should be a subfolder under outputdir
            anadir = os.path.join(outputdir, 'r_' + g_tool_name)
            input_args['anadir'] = anadir
            if not os.path.exists(anadir) and not ftest:
                os.mkdir(anadir)
        
        # this part will be improved later, particular when using a database
        if fcdb:
            import connect_db as cdb
            ss = cdb.connect_db(CONFIG_DICT['database'])
            query = ss.query(cdb.Cutoff_rg_alltrj).filter_by(sqid=seq)
            time_for_b = query.value(cdt)
            input_args['b'] = time_for_b
        else:
            input_args['b'] = 0                                       # default

        # particular to make_ndx
        if toa == 'g_make_ndx':
            ndx_id = CONFIG_DICT['ndx_input']                  # ndx_input_dict
            ndx_fd = CONFIG_DICT['ndx_format']                 # ndx_format_dict
            from pprint import pprint as pp
            input_args['ndx_input'] = ' '.join(
                [ndx_id[ndx_fd[f].format(**locals())] for f in ndx_fd]
                )

        # particular to sequence_spacing, maybe later toa need also to be
        # checked for other analysis, as well.
        if toa == 'sequence_spacing':
            from Mysys import read_mysys_dat
            mysys = read_mysys_dat()
            input_args['peptide_length'] = mysys[seq].len

        if btime:
            input_args['b'] = btime

        # generate the command that is gonna be executed
        cmd = g_tool(input_args)
        logf = os.path.join(logd, '{0}.log'.format(pf)) if logd else None
        yield (cmd, logf)

def main():
    # determine which function to call
    g_tool, ARGS = gai.target_the_type_of_analysis()
    g_tool_name =  g_tool.func_name   # directory will be named after func_name

    config_file = ARGS.config_file
    if not os.path.exists(config_file):
        raise ValueError('configuration file: {0} may not exist!'.format(config_file))
    config_dict = ConfigObj(config_file)

    SEQS = ARGS.SEQS if ARGS.SEQS else config_dict['system']['SEQS']
    CDTS = ARGS.CDTS if ARGS.CDTS else config_dict['system']['CDTS']
    TMPS = ARGS.TMPS if ARGS.TMPS else config_dict['system']['TMPS']
    NUMS = ARGS.NUMS if ARGS.NUMS else config_dict['system']['NUMS']

    dirchy_dict = config_dict['dirchy']
    directory_hierarchy = dirchy(SEQS, CDTS, TMPS, NUMS, dirchy_dict)

    # confirm outpudir path, if not specified either in cmd or in the
    # configuration file, 'R_OUTPUT" will be used in the current directory
    # to avoid scinet crash.
    if ARGS.outputdir:
        outputdir = ARGS.outputdir
    elif config_dict['data'].has_key('outputdir'):
        v = config_dict['data']['outputdir']
        if len(v) > 0 and v:                     # make sure v is not '' or None
            outputdir = v
        else:
            outputdir = 'R_OUTPUT'
    else:
        outputdir = 'R_OUTPUT'

    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    # parent_logd holds all the logs which keep the output of analysis tools
    parent_logd = os.path.join(outputdir, 'LOGS') 
    # just mkdir parent_logd no matter testing or not
    if not os.path.exists(parent_logd):
        os.mkdir(parent_logd)
                           
    logd = os.path.join(
        outputdir, 'LOGS', '{0}_log'.format(g_tool_name)
        ) if not ARGS.nolog else None

    if logd and not os.path.exists(logd):
        os.mkdir(logd)

    # now you have g_tool, g_tool_name, outputdir, logd, directory_hierarchy
    x = gen_input_args(g_tool, g_tool_name, outputdir, logd, directory_hierarchy,
                       ARGS.test, ARGS.cdb, ARGS.toa, ARGS.btime)
    gai.runit(x, ARGS.numthread, ARGS.test)

    separator =  "#" * 79
    print separator
    dd = ARGS.__dict__
    for k in sorted(dd):
        print "{0:>20s}:{1}".format(k, dd[k])
    print separator

if __name__ == "__main__":
    main()

