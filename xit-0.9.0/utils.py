import os
import re
import time
import shutil
import logging
logger = logging.getLogger(__name__)
import subprocess
import Queue
from threading import Thread
from collections import OrderedDict
from functools import update_wrapper

import tables
import numpy as np

"""
Here contains basic util functions, this module shall not import any other
local xit-specific modules
"""

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

def sem(vals):
    mean = np.mean(vals)
    p1 = sum((val - mean) ** 2 for val in vals)
    p2 = len(vals)
    p3 = p2 - 1
    return np.sqrt(p1 / p2) / np.sqrt(p3)

def sem3(ar):
    # equivalent to stats.sem(ar, axis=0) for 3D array
    # return ar.std(axis=0) / (ar.shape[0] - 1)

    A = np.zeros(ar.shape[1:])
    for i in range(ar.shape[1]): 
        for j in range(ar.shape[2]): 
            A[i][j]=sem(ar[:,i,j])
    return A

def gen_rc(n):
    """generate row and column numbers"""
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

def split(l, group_size):
    """split a list into n chunks"""
    n = group_size
    if len(l) <= n:
        logger.info(
            'the length of l ({0}) is less than the size of groups ({1}), so split not executed and returned l'.format(
                len(l), n))
        return l
    else:
        k = len(l) / n
        if k * n < len(l):
            k += 1                             # asure to include the remainder
        return [l[(i * n): ((i+1) * n)] for i in xrange(k)]

def float_params(d, *key_list):
    """
    this is not very great way of trying to do what json does

    key_list contains the names of properties as specified in the xit
    configuration file (e.g. xitconfig) that need to be converted to float
    """
    # overwrite old vals with floated ones
    d.update({k:float(d[k]) for k in key_list if k in d})
    return d

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

def get_dpp(cv):        # get deepest path, e.g. w300/sq1/00
    PATH_KEY_RE = re.compile('path\d+')
    dpk = max([p for p in cv.keys() if re.match(PATH_KEY_RE, p)], 
              key=lambda x: int(x[4:]))
    return cv[dpk]

def get_h5(A, C):
    if A.hdf5:
        hdf5 = A.hdf5
    else:
        hdf5 = C['hdf5']['filename']
    logger.info('reading h5: {0}'.format(hdf5))
    if not os.path.exists(hdf5):
        hdf5_title = C['hdf5']['filename']
        h5 = tables.openFile(hdf5, mode="w", title=hdf5_title)
    else:
        h5 = tables.openFile(hdf5, mode="a")
    return h5

def gen_output_filename(A, C):
    if A.output:
        return A.output
    fmt = A.output_format if A.output_format else 'png'
    prop, pt = get_prop(A), get_pt(A)           # pt: plot_type or plot2p_typen

    plots_dir = C['data']['plots']
    if not os.path.exists(plots_dir):
        os.mkdir(plots_dir)
    output = os.path.join(
        plots_dir, '{0}.{1}'.format('_'.join([pt, prop]), fmt))
    logger.info('saving to {0} ...'.format(output))
    return output

def get_anal_dd(C, anal_name):
    r = C.get('anal')
    if not r:
        logger.info('[anal] NOT found in {0}'.format(C.filename))
        return {}
    rr = r.get(anal_name)
    if not rr:
        logger.info('[[{0}]] NOT found in [anal]'.format(anal_name)) 
        return {}
    return rr

def get_prop_dd(C, prop_name):
    """
    get the configuration for a particular property (prop) in the plot section
    of .xitconfig
    """
    r = C.get('plot')
    if not r:
        logger.info('[plot] NOT found in {0}'.format(C.filename))
        return {}
    rr = r.get(prop_name)
    if not rr:
        logger.info('[[{0}]] NOT found in [plot] in {1}'.format(prop_name, C.filename))
        return {}
    logger.info('found [[{0}]] in [plot] in {1}'.format(prop_name, C.filename))
    return rr

def get_pt_dd(C, prop_name, pt_name):
    """get the configuration for plot type or plot2p type (pt) in the plots
    section of .xitconfig"""
    r = get_prop_dd(C, prop_name)
    if r:
        rr = r.get(pt_name)
        if rr:
            logger.info('found [[[{0}]]] in [[{1}]]'.format(pt_name, prop_name))
            return rr
        else:
            logger.info('[[[{0}]]] NOT found in [[{1}]]'.format(pt_name, prop_name))

    logger.info('starting looking into [plot2p] for [[[{0}]]]...'.format(pt_name))
    # assumed there will be not name overlap in plot and plot2p sections since
    # in the former, only one property is expected while in the later case, two
    # are.
    s = C.get('plot2p')
    if not s:
        logger.info('[plot2p] NOT found in {0}'.format(C.filename))
        return {}
    ss = s.get(prop_name)
    if not ss:
        logger.info('[[{0}]] NOT found in [plot2p] in {1}'.format(prop_name, C.filename))
        return {}
    sss = ss.get(pt_name)
    if not sss:
        logger.info('[[[{0}]]] NOT found in [[{1}]]'.format(pt_name, prop_name))
        return {}
    logger.info('found [[[{0}]]] in [[{1}]]'.format(pt_name, prop_name))
    return sss

def get_prop(A):
    """get the name of property or properties following the specific rule"""
    if hasattr(A, 'property'):
        prop = A.property
    elif hasattr(A, 'properties'):
        prop = '_'.join(A.properties)
    return prop

def get_pt(A):
    """get the name of A.plot_type or A.plot2p_type"""
    # comparing this function get_prop, it's ok to use for loop here because
    # there is no necessity to further process the value return by getattr or .
    for _ in ['plot_type', 'plot2p_type']:
        if hasattr(A, _):
            pt = getattr(A, _)
            return pt

def is_plot_type(f):
    """used as a decorator to label plot_type functions"""
    setattr(f, 'IS_PLOT_TYPE', 1)
    return f

def is_plot2p_type(f):
    setattr(f, 'IS_PLOT2P_TYPE', 1)
    return f

def get_col(c):
    """convert to correct color values"""
    return '#{0}'.format(c) if re.match('[A-F0-9]{6}', c) else c

# def is_transformable(f):
#     """if IS_TRANSFORMABLE, then can be transformed to a hdf5 file"""
#     setattr(f, 'IS_TRANSFORMABLE', 1)
#     return f
