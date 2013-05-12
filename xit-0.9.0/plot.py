import os
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

import numpy as np
from tables.exceptions import NoSuchNodeError

import prop
import utils
import plot_types

"""Normalization should happen here rather than during plotting!!!"""

def plot(A, C, core_vars):
    h5 = utils.get_h5(A, C)
    prop_obj = prop.Property(A.property)
    data = OrderedDict()
    grps = groupit(core_vars, prop_obj, A, C, h5)
    logger.info("Groups: {0}".format(grps.keys()))
    calc_fetch_or_overwrite(grps, prop_obj, data, A, C, h5)

    func = plot_types.PLOT_TYPES[A.plot_type]
    func(data, A, C)

def calc_fetch_or_overwrite(grps, prop_obj, data, A, C, h5):
    """data should be a empty OrderedDict"""
    for c, gk in enumerate(grps):
        logger.info('processing Group {0}: {1}'.format(c, gk))
        
        # ar: array
        for _ in ['plot_type', 'plot2p_type']:
            if hasattr(A, _):
                pt = getattr(A, _)               # pt: plot_type or plot2p_type
        ar_name = '{0}_{1}'.format(pt, prop_obj.name)                
        ar_where = os.path.join('/', gk)
        ar_whname = os.path.join(ar_where, ar_name)
        if h5.__contains__(ar_whname):
            if not A.overwrite:
                logger.info('fetching subdata from precalculated result')
                sda = h5.getNode(ar_whname).read()     # sda: subdata
            else:
                logger.info('overwriting old subdata with new ones')
                _ = h5.getNode(ar_whname)
                _.remove()
                ar = calcit(grps[gk], gk, prop_obj, h5, A, C)
                h5.createArray(where=ar_where, name=ar_name, object=ar)
                sda = ar
        else:
            logger.info('Calculating subdata...')
            ar = calcit(grps[gk], gk, prop_obj, h5, A, C)
            if ar.dtype.name != 'object':
                # cannot be handled by tables yet, but it's fine not to store
                # it because usually object is a combination of other
                # calculated properties, which are store, so fetching them is
                # still fast
                h5.createArray(where=ar_where, name=ar_name, object=ar)
            else:
                logger.info('"{0}" dtype number array CANNNOT be stored in h5'.format(ar.dtype.name))
            sda = ar
        data[gk] = sda

def calcit(grp, gk, prop_obj, h5, A, C):
    # prop_dd may contain stuffs like denorminators, etc.

    prop_dd = utils.get_prop_dd(C, prop_obj.name)
    args = [h5, gk, grp, prop_obj, prop_dd, A, C]
    
    # the name of pt MUST follow those function names in files in ./plot_types
    # or .plot2p_types
    pt = utils.get_pt(A) 
    if pt in ['bars', 'grped_bars', 'xy', 'grped_xy']:
        return calc_means(*args)
    elif pt in ['alx', 'grped_alx', 'mp_alx']:
        return calc_alx(*args)
    elif pt in ['distr', 'grped_distr']:
        return calc_distr(*args)
    elif pt == 'grped_distr_ave':
        return calc_distr_ave(*args)
    elif pt == 'map':
        return calc_map(grp, prop_obj)
    elif pt == 'pmf':
        return calc_pmf(grp, prop_obj, A, C)
    else:
        raise IOError('Do not know how to calculate "{0}"'.format(pt))

def calc_means(h5, gk, grp, prop_obj, prop_dd, A, C):
    grp_tb = fetch_grp_tb(h5, grp, prop_obj.name)
    _l = []
    for tb in grp_tb:
        _ = tb.read(field=prop_obj.ifield).mean()
        _l.append(_)

    if 'denorminators' in prop_dd:
        denorm = float(prop_dd['denorminators'][gk])
        return np.array([np.mean(_l) / denorm, utils.sem(_l) / denorm])

    return np.array([np.mean(_l), utils.sem(_l)])

def calc_distr(h5, gk, grp, prop_obj, prop_dd, A, C):
    grp_tb = fetch_grp_tb(h5, grp, prop_obj.name)
    min_len = min(tb.read(field='time').shape[0] for tb in grp_tb)
    _l = []
    for tb in grp_tb:
        _l.append(tb.read(field=prop_obj.ifield)[:min_len])
    _la = np.array(_l)

    # grped_distr_ave is a variant of grped_distr
    special_cases = {'grped_distr_ave': 'grped_distr'}
    pt_dd = utils.get_pt_dd(
        C, A.property, 
        special_cases.get(A.plot_type, A.plot_type))

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

def calc_distr_ave(*args):
    distrs = calc_distr(*args)
    aves = calc_means(*args)
    return np.array([distrs, aves])

def calc_alx(h5, gk, grp, prop_obj, prop_dd, A, C):
    grp_tb = fetch_grp_tb(h5, grp, prop_obj.name)
    # x assumed to be FIELD_0_NAME
    tb0 = grp_tb[0]
    xf = tb0._f_getAttr('FIELD_0_NAME') # xf: xfield, and it's assumed to be
                                        # the same in all tabls in the grp_tb
    min_len = min(tb.read(field=xf).shape[0] for tb in grp_tb)
    _l = []
    ref_col = grp_tb[0].read(field=xf)[:min_len]
    for tb in grp_tb:
        col1 = tb.read(field=xf)[:min_len]
        assert (col1 == ref_col).all() == True
        col2 = tb.read(field=prop_obj.ifield)[:min_len]
        _l.append(col2)
        _a = np.array(_l)

    if 'xdenorm' in prop_dd:
        ref_col = ref_col / float(prop_dd['xdenorm'])
    _aa = np.array([ref_col, _a.mean(axis=0),
                    [utils.sem(_a[:,i]) for i in xrange(len(_a[0]))]])
    res = block_average(_aa)
    return res

def calc_map(grp, prop_obj):
    _l = []
    for tb in grp:                              # it could be array
        _l.append(tb)
    # no need to normalize when plotting a map!
    # norm  = prop_obj.norm('sq1') # dirty
    return np.array(_l).mean(axis=0)

def calc_pmf(grp, prop_obj, A, C):
    dd = C['plot'][A.property][A.plot_type]
    if 'bins' not in dd:
        raise ValueError('bins not found in {0}, but be specified when plotting pmf'.format(C.name))
    subgrps = utils.split(grp, 4)                         # split into 4 chunks
    da = []
    for sp in subgrps:
        bn, psm, pse = calc_distr(sp, prop_obj, A, C)
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


def fetch_grp_tb(h5, grp, prop_name):
    """fetch tbs bashed on where values in grp"""
    grp_tb = []
    for where in grp:
        tb = fetch_tb(h5, where, prop_name)
        if tb:
            grp_tb.append(tb)
    return grp_tb

def fetch_tb(h5, where, prop_name):
    try:
        # this is slow, so DON'T call it unless really necessary
        # ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        # 961/481    0.003    0.000    4.711    0.010 file.py:1061(getNode)
        # 10085/485    0.022    0.000    4.707    0.010 file.py:1036(_getNode)
        tb = h5.getNode(where, prop_name)
        return tb
    except NoSuchNodeError:
        logger.info('Dude, NODE "{0}" DOES NOT EXIST in the table!'.format(
                os.path.join(where, prop_name)))

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

@utils.timeit
def groupit(core_vars, prop_obj, A, C, h5):
    """
    grouping all the tables by grptoken (group token) specified in the commnand
    line
    """
    logger.info('grouping... by token: {0}'.format(A.grptoken))
    grptoken = A.grptoken
    grps = OrderedDict()                                    # grped data

    for cv in core_vars:
        grpid = cv[grptoken]
        if grpid not in grps:
            grps[grpid] = []
        where = os.path.join('/', utils.get_dpp(cv))
        grps[grpid].append(where)
        # try:
        #     # this is slow:
        #     # ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        #     # 961/481    0.003    0.000    4.711    0.010 file.py:1061(getNode)
        #     # 10085/485    0.022    0.000    4.707    0.010 file.py:1036(_getNode)
        #     tb = h5.getNode(where, prop_obj.name)
        #     grps[grpid].append(tb)
        # except NoSuchNodeError:
        #     logger.info('Dude, NODE "{0}" DOES NOT EXIST in the table!'.format(
        #             os.path.join(where, prop_obj.name)))
    return grps
