import re
import os
import time
import shutil
import argparse
import subprocess
import Queue
import logging
L = logging.info
from threading import Thread
from collections import OrderedDict
from functools import update_wrapper

import tables
import numpy as np

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        res = method(*args, **kw)
        te = time.time()
        # cannot use logging.info: guess due to namespacing problem
        print '--- spent: {0:.1e}s on {1}'.format(te - ts, method.__name__)
        # print '--- spent: {0}    on {1}\n'.format(
        #         time.strftime('%H:%M:%S', time.gmtime(delta_time)),
        #         method.__name__)
        return res
    return timed

def backup_file(f):
    if os.path.exists(f):
        dirname = os.path.dirname(f)
        basename = os.path.basename(f)
        count = 1
        rn_to = os.path.join(
            dirname, '#' + basename + '.{0}#'.format(count))
        while os.path.exists(rn_to):
            count += 1
            rn_to = os.path.join(
                dirname, '#' + basename + '.{0}#'.format(count))
        print "BACKING UP {0} to {1}".format(f, rn_to)
        shutil.copy(f, rn_to)
        return rn_to
        print "BACKUP FINISHED"


class convert_vars(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        final = []
        for value in values:
            subfinal = []
            svalue = value.split()
            for val in svalue:
                # not trivial a regex that works!
                mat = re.search('([a-z]*)((?:[0-9]+|\[\d+-\d+\])?)', val)
                if mat:                                     # mat: match
                    prefix, num = mat.groups()
                    if num == '':
                        subfinal.append(prefix)
                    else:
                        mmat = re.search('\[(\d+)-(\d+)\]', num)
                        if mmat:                              # mmat: another match
                            min_, max_ = mmat.groups()
                            l = max([len(min_), len(max_)])
                            fmt = '{{0}}{{1:0{l}d}}'.format(l=l)
                            min_, max_ = (int(i) for i in mmat.groups())
                            res = [fmt.format(prefix, i) for i in xrange(min_, max_ + 1)]
                            subfinal.extend(res)
                        else:
                            fmt = '{{0}}{{1:0{l}d}}'.format(l=len(num))
                            subfinal.append(fmt.format(prefix, int(num)))
                else:
                    raise ValueError('unkown input: {0}'.format(val))
            final.append(subfinal)
        setattr(namespace, self.dest, final)

class verify_xy(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.plot_type != 'xy':
            raise ValueError('--xyp should be specified only when doing --plot_type xy')
        if len(values) != 2:
            raise ValueError('values of --xyp must be two. e.g. "upup unun"')
        setattr(namespace, self.dest, values)

@timeit
def get_args(args_to_parse=None):
    parser = argparse.ArgumentParser(description="xit helps you prepare, manage and analyze your simulations")
    subparsers = parser.add_subparsers(title='subcommands')

    prep_parser = subparsers.add_parser('prep', help='used during simulation preparation')
    mgrp = prep_parser.add_mutually_exclusive_group()
    mgrp.add_argument('--mkdir', action='store_true')
    mgrp.add_argument('--link_gro', action='store_true')
    mgrp.add_argument('--sed_0_jobsub_sh', action='store_true')
    mgrp.add_argument('--qsub_0_jobsub_sh', action='store_true')
    mgrp.add_argument('--sed_0_mdrun_sh', action='store_true')
    mgrp.add_argument('--qsub_0_mdrun_sh', action='store_true')

    anal_parser = subparsers.add_parser(
        'anal', help='do different sorts of analysis')
    anal_parser.add_argument('--numthreads', default=16, help='number of threads')
    anal_parser.add_argument('--test', action='store_true', help='if test, print the cmd without executing it')
    anal_parser.add_argument('--nolog', action='store_true', help='disable logging, output to stdout')
    anal_parser.add_argument('--extend', help='for extending tpr, should be time in ps, not # of steps')
    anal_parser.add_argument('-b', default=0, help='gromacs -b')
    anal_parser.add_argument('--opt_arg', help=('this is used for tool specific arguments specified'
                                                'in the .xitconfig file (e.g. var1, var2, or var3)'))

    transform_parser = subparsers.add_parser(
        'transform', help=('transform the file formats from analysis step (e.g. xvg) to hdf5 format, '
                           'if the previous one is in hdf5 already, then this step is unecessary.'))
    transform_parser.add_argument('-t' , '--filetype', default='xvg', help='self-explained, e.g. xvg')
    transform_parser.add_argument('--overwrite', action='store_true', help='overwrite previous data')
    transform_parser.add_argument('--init_hdf5', action='store_true', help='initialize hdf5, creating dirs, etc.')

    plot_parser = subparsers.add_parser(
        'plot', help='postprocess the results from analysis and illustrate it via plotting')
    plot_parser.add_argument('--plot_type', help='simple_bar, alx, etc')
    # plot_parser.add_argument('--scale', action='store_true', help='scale to 1, when map plotting is not obvious')
    plot_parser.add_argument('-o', '--output', help='output file')
    # shouldn't be used, instead put it in the .xitconfig --2013-05-09
    # plot_parser.add_argument('--normid', help='var1, etc')

    plot2p_parser = subparsers.add_parser(
        'plot2p', help='similar to plot, but handles two properties at the same time')
    plot2p_parser.add_argument('--plot_type', help='e.g. xy, etc')
    plot2p_parser.add_argument('-a' , '--analysis', nargs='+', action=verify_xy,
                               help=('added MULTIPLE properties, which is different '
                                     'than a single property in plot. e.g. "upup unun"'))

    for p in [plot_parser, plot2p_parser]:
        p.add_argument('--grptoken', default='mena', help='how to group the original  directories? e.g. path2')
        p.add_argument('--merge', action='store_true', help='merge all plots in one ax')
        p.add_argument('--overwrite', action='store_true', help='overwrite previous postprocess data')

    for p in [prep_parser, anal_parser, transform_parser, plot_parser, plot2p_parser]:
        # forget what the following two lines mean ---2013-05-09
        # f is used to add global_args, it does not work with argparse to put
        # --vars in right after argparse.ArgumentParser, which is strange
        p.add_argument('-v', '--vars', nargs='+', action=convert_vars,
                       help='list of vars, as defined in the .xit file, command line options override .xit')
        p.add_argument('-g', '--config', default='.xitconfig', help='specify the config option if not default')
        p.add_argument('--nobackup', action='store_true', help="don't back the file to speed up analysis")
        p.add_argument('--loglevel', default='info', help="don't back the file to speed up analysis")

    from methods import METHODS
    for p in [anal_parser, transform_parser, plot_parser]:
        p.add_argument('-a' , '--analysis', help='self-explained, e.g. {0}'.format(METHODS.keys()))

    for p in [anal_parser, transform_parser, plot_parser, plot2p_parser]:
        p.add_argument('--hdf5', help='specify the .h5 file to use if not configured in .xitconfig')

    args = parser.parse_args(args_to_parse)
    return args

def gen_id_paths_r(vars_, dir_templates, id_template='', result=[], **kw):
    """_r means recursion"""
    if not vars_:
        # pnames: path names
        pnames = [tmp.format(**kw) for tmp in dir_templates]
        tmp_l = [id_template.format(**kw)] if id_template else [] # temporary list
        for i in xrange(len(pnames)):
            tmp_l.append(os.path.join(*pnames[0:i+1]))
        result.append(tmp_l)
    else:
        k, val = vars_.popitem()
        for v in val:
            kw_copy = {i:kw[i] for i in kw}
            kw_copy.update({k:v})
            vars_copy = {i:vars_[i] for i in vars_}
            gen_id_paths_r(vars_copy, dir_templates, id_template, **kw_copy)
    return result

def gen_core_vars_r(vars_, dir_tmpls, id_tmpl='', result=[], **kw):
    """_r means recursion"""
    if not vars_:
        # cv: core vars
        cv = {}
        dirnames = {_:dir_tmpls[_].format(**kw) for _ in dir_tmpls}
        dirnames = OrderedDict(sorted(dirnames.items(), key=lambda i: i[0]))
        cv.update(dirnames)
        cv.update(id_=id_tmpl.format(**kw))
        cv.update(kw)
        pathnames = dirnames.values()
        for i in xrange(len(pathnames)):
            cv.update({'path{0}'.format(i+1):os.path.join(*pathnames[0:i+1])})
        result.append(cv)
    else:
        k, val = vars_.popitem()
        for v in val:
            kw_copy = {i:kw[i] for i in kw}
            kw_copy.update({k:v})
            vars_copy = {i:vars_[i] for i in vars_}
            gen_core_vars_r(vars_copy, dir_tmpls, id_tmpl, **kw_copy)
    return result

def get_vars(A, C):
    CS = C['systems']
    if A.vars:
        vars_ = {'var{0}'.format(k+1):v for k, v in enumerate(A.vars)}
    else:
        vars_ = {k:CS[k] for k in CS.keys() if re.match('var[0-9]+', k)}
    vars_ = OrderedDict(sorted(vars_.items(), key=lambda i: i[0]))
    return vars_

def get_dir_tmpls(A, C):
    CS = C['systems']
    dir_tmpls = {k:CS[k] for k in CS.keys() if re.match('dir[0-9]+', k)}
    # sorted dir_tmpls by keys, the number in particular
    dir_tmpls = OrderedDict(sorted(dir_tmpls.items(), key=lambda t:t[0]))
    return dir_tmpls

# def gen_paths(dirs, dirname='', result=[]):
#     if not dirs:
#         result.append(dirname)
#     else:
#         d = dirs.pop(0)
#         for i in d:
#             dn = os.path.join(dirname, i)
#             # a copy for each branch
#             dirs_copy = [x for x in dirs]
#             gen_paths(dirs_copy, dirname=dn)
#     return result

def gen_io_files(target_dir, pf):
    """
    Generalizing input files specific for gromacs tools, default naming
    """

    io_files = dict(
        xtcf = os.path.join(
            target_dir, '{pf}_md.xtc'.format(pf=pf)),
        centerxtcf = os.path.join(
            target_dir, '{pf}_center.xtc'.format(pf=pf)),
        orderxtcf = os.path.join(
            target_dir, '{pf}_order.xtc'.format(pf=pf)),
        ordergrof = os.path.join(
            target_dir, '{pf}_order.gro'.format(pf=pf)),
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
    return io_files


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

def get_dpp(cv):              # get deepest path
    # cv a set of core variables for a simple replica
    PATH_KEY_RE = re.compile('path\d+')
    dpk = max([p for p in cv.keys() if re.match(PATH_KEY_RE, p)], 
              key=lambda x: int(x[4:]))
    return cv[dpk]

def get_h5(A, C):
    if A.hdf5:
        hdf5 = A.hdf5
    else:
        hdf5 = C['hdf5']['filename']
    L('reading h5: {0}'.format(hdf5))
    if not os.path.exists(hdf5):
        hdf5_title = C['hdf5']['filename']
        h5 = tables.openFile(hdf5, mode="w", title=hdf5_title)
    else:
        h5 = tables.openFile(hdf5, mode="a")
    return h5

def sem(vals):
    mean = np.mean(vals)
    p1 = sum((val - mean) ** 2 for val in vals)
    p2 = len(vals)
    p3 = p2 - 1
    return np.sqrt(p1 / p2) / np.sqrt(p3)

def sem3(ar):
    # equivalent to stats.sem(ar, axis=0) for 3D array
    A = np.zeros(ar.shape[1:])
    for i in range(ar.shape[1]): 
        for j in range(ar.shape[2]): 
            A[i][j]=sem(ar[:,i,j])
    return A

def gen_rc(n):
    c = int(np.sqrt(n))
    r = c
    if c * r == n:
        return c, r
    else:         # r * c < n                                                  
        r = r + 1
        if r * c < n:
            return c, r+1, 
        else:
            return c, r

def split(l, n):
    """split a list into n chunks"""
    if len(l) <= n:
        return l
    else:
        idx = len(l) / n
        if idx * n < len(l):
            idx += 1                           # asure to include the remainder
        return [l[i:idx * (i+1)] for i in xrange(idx)]

def gen_output_filename(A, C):
    if A.output:
        return A.output
    else:
        output = os.path.join(
            C['data']['plots'], 
            '{0}.png'.format('_'.join([A.plot_type, A.analysis])))
        return output

def float_params(d, *key_list):
    """
    this is not very great way of trying to do what json does

    key_list contains the names of properties as specified in the xit
    configuration file (e.g. xitconfig) that need to be converted to float
    """
    # overwrite old vals with floated ones
    d.update({k:float(d[k]) for k in key_list if k in d})
    return d
            
