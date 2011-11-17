#!/usr/bin/env python

import re
import os
import sys
import glob
from string import Template
from optparse import OptionParser
import g_ana_org as gao
import g_ana_basic as gab
import g_ana_rdf as gar
import g_ana_int as gai
import g_ana_other as gat

AVAILABLE_ANALYSIS = []
for g in [gao, gab, gar, gai, gat]:
    AVAILABLE_ANALYSIS += getattr(g, '__all__')

def outline(g_tool):
    target_dirs = glob.glob(DIR_PATTERN)
    kwargs_list = []
    for k, target_dir in enumerate(target_dirs):
        basename = os.path.basename(target_dir)
        kwargs = {'g_tool' : g_tool.func_name,
                  'pf' : basename, 
                  'seq' : basename[:3],
                  'cdt': basename[3],
                  'b' : 40000,
                  'anadir' : ANADIR,
                  'target_dir' : target_dir,
                  'ndx_inputs' : NDX_INPUTS}
        
        input_files = gao.gen_input_files(target_dir, basename)
        kwargs.update(input_files)

        if (g_tool.__module__ ==  'g_ana_int' or
            g_tool.__module__ == 'g_ana_rdf'):
            # determine the interaction groups & cutoff
            template = re.compile('[uv][pn][uv][pn]')
            k = template.search(g_tool.func_name).group()
            kwargs.update(igrp = gai.inter_groups_matrix()[k],
                          icff = gai.inter_cutoffs()[k])

        if (not g_tool.__module__ == 'g_ana_org'
            or not g_tool.__module__ == 'main'):
            kwargs.update(dict(
                    outputdir = os.path.join(
                        ANADIR, 'r_' + g_tool.func_name)))
            gao.try_mkdir(kwargs['outputdir'])

        kwargs_list.append(kwargs)
    gao.runit(g_tool, kwargs_list, OPTIONS, LOGDIR)

def parse_cmd(args):
    parser = OptionParser(usage='g_ana.py -s "sq[1-2]" -c "[mw]" -n "[01][0-9]" -a="check_target_dirs"')
    parser.add_option('-s', '--seq', type='str', dest='seq', default='sq[1-6]')
    parser.add_option('-c', '--cdt', type='str', dest='cdt', default='[wm]')
    parser.add_option('-n', '--num', type='str', dest='num', default=None)
    parser.add_option('-a','--type_of_analysis', type='str', dest='toa', default=None, 
                      help='available_options:\n%r' % AVAILABLE_ANALYSIS )
    parser.add_option('--test', dest='test', action='store_true', default=False)
    parser.add_option('--nolog', dest='nolog', action='store_true', default=False)
    (options, args) = parser.parse_args(args)
    return options

if __name__ == '__main__':
    OPTIONS = parse_cmd(sys.argv[1:])
    pwd = os.environ['PWD']
    d = dict(_SEQ_=OPTIONS.seq, _CDT_=OPTIONS.cdt, _NUM_=OPTIONS.num)

    configf = os.path.join(pwd, '.g_ana.cfg')
    configs = gao.configparse(configf)

    ANADIR = gao.try_mkdir(configs.get('ana_dir_name', 'default_ana_dir'))
    LOGDIR = gao.try_mkdir(configs.get('log_dir_name', 'default_log_dir'))

    DIR_PATTERN = Template(configs['absolute_dir_pattern']).substitute(d)
    NDX_INPUTS = dict([ i for i in configs.iteritems() 
                        if i[0].startswith('NDX_') ])
    print DIR_PATTERN

    if OPTIONS.toa == 'g_make_ndx':
        outline(gao.g_make_ndx)

    if OPTIONS.toa == 'rg_CA':
        outline(gab.rg_CA)

    elif OPTIONS.toa == 'uxi':
        # outline(gai.upup)
        # outline(gai.upun)
        # outline(gai.unun)
        
        outline(gai.upvp)       # even initiating the hb groups takes a lot of time 
        # outline(gai.upvn)
        # outline(gai.unvp)
        # outline(gai.unvn)
    elif OPTIONS.toa == 'ux_rdf':
        outline(rdf_upup)
        outline(rdf_upun)
        outline(rdf_unun)
        
        outline(rdf_upvp)
        outline(rdf_upvn)
        outline(rdf_unvp)
        outline(rdf_unvn)
    # elif options.toa == 'vvi':
    #     pass
    #     # outline(vpvp)
    #     # outline(vpvn)
    #     # outline(vnvn)
    # elif options.toa == 'vv_rdf':
    #     pass
    #     # outline(rdf_vpvp)
    #     # outline(rdf_vpvn)
    #     # outline(rdf_vnvn)
    # elif options.toa == 'g_rama':
    #     outline(g_rama)
