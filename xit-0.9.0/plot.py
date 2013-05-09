import sys
import os
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

import numpy as np
from tables.exceptions import NoSuchNodeError

import prop
import utils

import plot_types

class UnrecoganizedPlotTypeError(Exception):
    pass

def plot(A, C, core_vars):
    h5 = utils.get_h5(A, C)
    pt_obj = prop.Property(A.analysis)
    grps = groupit(A, C, core_vars, h5)
    logger.info("Groups: {0}".format(grps.keys()))

    data = OrderedDict()
    for k, gk in enumerate(grps):
        logger.info('processing Group {0}: {1}'.format(k, gk))
        # ar: array
        ar_where = os.path.join('/', gk)
        ar_name = '{0}_{1}'.format(A.plot_type, A.analysis)
        ar_whname = os.path.join(ar_where, ar_name)
        if h5.__contains__(ar_whname):
            if not A.overwrite:
                logger.info('fetching subdata from precalculated result')
                sda = h5.getNode(ar_whname).read()     # sda: subdata
            else:
                logger.info('overwriting old subdata with new ones')
                _ = h5.getNode(ar_whname)
                _.remove()
                ar = calcit(grps[gk], pt_obj, gk, A, C)
                h5.createArray(where=ar_where, name=ar_name, object=ar)
                sda = ar
        else:
            logger.info('Calculating subdata...')
            ar = calcit(grps[gk], pt_obj, gk, A, C)
            if ar.dtype.name != 'object':
                # cannot be handled by tables yet, but it's fine not to store
                # it because usually object is a combination of other
                # calculated properties, which are store, so fetching them is
                # still fast
                h5.createArray(where=ar_where, name=ar_name, object=ar)
            sda = ar
        data[gk] = sda

    func = plot_types.PLOT_TYPES[A.plot_type]
    func(data, A, C)

def calcit(grp, pt_obj, gk, A, C):
    # the name for plot_types MUST follow those function names in files in
    # ./plot_types
    if A.plot_type in ['simple_bar', 'grped_bars']:
        return calc_simple_bar(grp, pt_obj)
    elif A.plot_type == 'alx':
        return calc_alx(grp, pt_obj)
    elif A.plot_type == 'map':
        return calc_map(grp, pt_obj)
    elif A.plot_type in ['distr', 'grped_distr']:
        return calc_distr(grp, pt_obj, A, C)
    elif A.plot_type == 'pmf':
        return calc_pmf(grp, pt_obj, A, C)
    elif A.plot_type == 'grped_distr_ave':
        return calc_distr_ave(grp, pt_obj, A, C)
    else:
        raise IOError('Do not know how to calculate "{0}"'.format(A.plot_type))
    
def calc_map(grp, pt_obj):
    _l = []
    for tb in grp:                              # it could be array
        _l.append(tb)
    # no need to normalize when plotting a map!
    # norm  = pt_obj.norm('sq1') # dirty
    return np.array(_l).mean(axis=0)

def calc_alx(grp, pt_obj):
    min_len = min(tb.read(field='time').shape[0] for tb in grp)
    _l = []
    ref_col = grp[0].read(field='time')[:min_len]
    for tb in grp:
        col1 = tb.read(field='time')[:min_len]
        assert (col1 == ref_col).all() == True
        col2 = tb.read(field=pt_obj.ifield)[:min_len]
        _l.append(col2)
        _a = np.array(_l)
    _aa = np.array([
            ref_col / 1000,                         # ps => ns
            _a.mean(axis=0),
            [utils.sem(_a[:,i]) for i in xrange(len(_a[0]))]])
    res = block_average(_aa)
    return res

def block_average(a, n=100):
    """a is a mutliple dimension array, n is the max number of data points desired"""
    if a.shape[1] < n:
        return a
    else:
        bs = int(a.shape[1] / n)                            # bs: block size
        print a.shape[1]
        if bs * n < a.shape[1] - 1:                         # -1 is math detail
            bs = bs + 1
        print 'block size: {0}, # of blocks: {1}'.format(bs, n)
        return np.array([a[:,bs*(i-1):bs*i].mean(axis=1) 
                         for i in xrange(1, n+1)]).transpose()

def calc_simple_bar(grp, pt_obj):
    _l = []
    for tb in grp:
        _ = tb.read(field=pt_obj.ifield).mean()
        _l.append(_)
    return np.array([np.mean(_l), utils.sem(_l)])

def calc_distr(grp, pt_obj, A, C, **kw):
    min_len = min(tb.read(field='time').shape[0] for tb in grp)
    _l = []
    for tb in grp:
        _l.append(tb.read(field=pt_obj.ifield)[:min_len])
    _la = np.array(_l)

    # CONCISE VERSION:
    if A.plot_type == 'grped_distr_ave':
        # grped_distr_ave is a variant of grped_distr
        pt_dd = C['plots'][A.analysis]['grped_distr']
    else:
        pp_dd = C['plots'][A.analysis][A.plot_type]

    # VERBOSE BUT EXPLICIT VERSION
    # if A.plot_type == 'distr':
    #     pt_dd = C['plots'][A.analysis]['distr']
    # elif A.plot_type in ['grped_distr', 'grped_distr_ave']:
    #     pt_dd = C['plots'][A.analysis]['grped_distr']
    # else:
    #     pp_dd = C['plots'][A.analysis][plot_type]

    if 'bins' in pt_dd:
        i, j, s = [float(_) for _ in pt_dd['bins']]
        bins = np.arange(i, j, s)
    else:
        # assume usually 36 bins would be enough
        bins = np.linspace(_la.min(), _la.max(), 36)

    ps = []                             # probability distributions for each tb
    for _ in _la:
        p, _ = np.histogram(_, bins, normed=False)          # probability
        p = p / float(sum(p))
        ps.append(p)
    ps = np.array(ps)

    bn = (bins[:-1] + bins[1:]) / 2.             # to gain the same length as psm, pse
    psm = ps.mean(axis=0)
    pse = [utils.sem(ps[:,i]) for i in xrange(len(ps[0]))]
    pse = np.array(pse)
    return np.array([bn, psm, pse])

def calc_distr_ave(grp, pt_obj, A, C, **kw):
    distrs = calc_distr(grp, pt_obj, A, C)
    aves = calc_simple_bar(grp, pt_obj)
    return np.array([distrs, aves])
    # the data structure can be confusing
    # sys.exit(1)
    # return np.array([distrs, aves])

def calc_pmf(grp, pt_obj, A, C):
    dd = C['plot'][A.analysis][A.plot_type]
    if 'bins' not in dd:
        raise ValueError('bins not found in {0}, but be specified when plotting pmf'.format(C.name))
    subgrps = utils.split(grp, 4)                         # split into 4 chunks
    da = []
    for sp in subgrps:
        bn, psm, pse = calc_distr(sp, pt_obj, A, C)
        pmf, pmf_e = prob2pmf(psm, max(psm), pse)
        sub_da = np.array([bn, pmf, pmf_e])
        da.append(sub_da)
    return np.array(da)

def prob2pmf(p, max_p, e=None):
    """
    p: p_x
    max_p: p_x0
    e: variance of p_x, used to calc error propagation

    convert the probability of e2ed to potential of mean force
    """

    T = 300                                                 # Kelvin
    # R = 8.3144621                                           # J/(K*mol)
    R = 8.3144621e-3                                        # KJ/(K*mol)
    # R = 1.9858775                                           # cal/(K*mol)
    # pmf = - R * T * np.log(p / float(max_p))

    # k = 1.3806488e-23                         # Boltzman constant J*K-1
    pmf = - R * T * np.log(p / float(max_p))  # prefer to use k and Joule
                                              # instead so I could estimate the
    if e is not None:
        e = e
        # Now, calc error propagation
        # since = pmf = -R * T * ln(p_x / p_x0)
        # First, we calc the error of (p_x / p_x0)
        # error_of_p_x_divided_by_p_x0 = e**2 / p_x0**2
        pmf_e = -R * T * e / p
        return pmf, pmf_e
    else:
        return pmf

@utils.timeit
def groupit(A, C, core_vars, h5):
    """grouping all the tables by grptoken (group token) specified in the commnand line"""
    logger.info('grouping... by token: {0}'.format(A.grptoken))
    grptoken = A.grptoken
    grps = OrderedDict()                                    # grped data
    for cv in core_vars:
        grpid = cv[grptoken]
        if grpid not in grps:
            grps[grpid] = []
        where = os.path.join('/', utils.get_dpp(cv))
        try:
            tb = h5.getNode(where, A.analysis)
            grps[grpid].append(tb)
        except NoSuchNodeError:
            logger.info('Dude, NODE "{0}" DOES NOT EXIST in the table!'.format(
                    os.path.join(where, A.analysis)))
    return grps
