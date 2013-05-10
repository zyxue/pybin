import os
import logging
logger = logging.getLogger(__name__)

import numpy as np
import matplotlib.pyplot as plt

import utils

@utils.is_plot_type
def distr(data, A, C, **kw):
    """data: is an OrderedDict"""
    logger.info('start plotting distr...')

    fig = plt.figure(figsize=(12,9))
    pt_dd = C['plots'][A.analysis][A.plot_type]
    if A.merge:
        ax = fig.add_subplot(111)
        for c, gk in enumerate(data.keys()):
            da = data[gk]
            params = get_params(gk, pt_dd)
            ax.plot(da[0], da[1], **params)
            # facecolor uses the same color as ax.plot
            ax.fill_between(da[0], da[1]-da[2], da[1]+da[2], 
                            where=None, facecolor=params['color'], alpha=.3)
        decorate_ax(ax, pt_dd)
    else:
        col, row = utils.gen_rc(len(data.keys()))
        logger.info('col: {0}, row; {1}'.format(col, row))
        for c, gk in enumerate(data.keys()):
            ax = fig.add_subplot(row, col, c+1)
            da = data[gk]
            params = get_params(gk, pt_dd)
            # ax.errorbar(da[0], da[1], yerr=da[2], **params)
            ax.plot(da[0], da[1], **params)
            ax.fill_between(da[0], da[1]-da[2], da[1]+da[2], 
                            where=None, facecolor=params.get('color'), alpha=.3)

            decorate_ax(ax, pt_dd)

    plt.savefig(utils.gen_output_filename(A, C))

def get_params(gk, pt_dd):
    params = {}
    if 'colors' in pt_dd:
        params['color'] = pt_dd['colors'][gk]
    if 'legends' in pt_dd:
        params['label'] = pt_dd['legends'][gk]
    else:
        params['label'] = gk
    return params

def decorate_ax(ax, pt_dd):
    leg = ax.legend(loc='best')
    ax.grid(which="major")
    if 'xlim' in pt_dd: 
        ax.set_xlim(**utils.float_params(pt_dd['xlim'], 'left', 'right'))
    if 'ylim' in pt_dd:
        ax.set_ylim(**utils.float_params(pt_dd['ylim'], 'bottom', 'top'))
    if 'xlabel' in pt_dd: ax.set_xlabel(pt_dd['xlabel'])
    if 'ylabel' in pt_dd: ax.set_ylabel(pt_dd['ylabel'], labelpad=10)
    if 'xscale' in pt_dd: ax.set_xscale(pt_dd['xscale'])

    if 'legend_linewidth' in pt_dd:
        for l in leg.legendHandles:
            l.set_linewidth(float(pt_dd['legend_linewidth']))


def sliceit(l, b, e):
    l_t = l.transpose()          # (n,3) multi-dimensional data
    s_l = l_t[b:e].transpose()   # (3,n) multi-dimensional data
    return s_l

def pmf(data, A, C, **kw):
    logger.info('start plotting pmf...')

    pt_dd = C['plot'][A.analysis][A.plot_type]

    fs = (float(i) for i in pt_dd['figsize']) if 'figsize' in pt_dd else (12,9)
    fig = plt.figure(figsize=fs)

    if A.merge:
        ax = fig.add_subplot(111)
        for k, gk in enumerate(data.keys()):
            # DIM of da: (x, 3, y), where x: # of replicas; y: # of bins
            da = data[gk]
            pre_pmfm = da.mean(axis=0)                  # means over x, DIM: (3, y)
            pre_pmfe = utils.sem3(da)                   # sems  over x, DIM: (3, y)

            if 'pmf_cutoff' in pt_dd:
                cf = float(pt_dd['pmf_cutoff'])
                bs, es = filter_pmf_data(pre_pmfm, cf)       # get slicing indices
            else:
                bs, es = filter_pmf_data(pre_pmfm)

            bn, pmfm, _ = sliceit(pre_pmfm, bs, es)             # bn: bin; pmfm: pmf mean
            bne, pmfe, _ = sliceit(pre_pmfe, bs, es)            # bne: bin err; pmfe: pmf err

            # pmf sem, equivalent to stats.sem(da, axis=0)
            pmfe = sliceit(pre_pmfe, bs, es)[1] # tricky: 1 corresponds err of pmf mean

            # now, prepare the errobars for the fit
            _pfits, _ks, _l0s = [], [], []
            for subda in da:
                sliced = sliceit(subda, bs, es)
                bn, pm, pe = sliced
                a, b, c = np.polyfit(bn, pm, deg=2)
                _pfv = parabola(bn, a, b, c)                    # pfv: pmf fit values
                _pfits.append(_pfv)
                _ks.append(convert_k(a))
                _l0s.append(-b/(2*a))

            _pfit = np.mean(_pfits, axis=0)
            _k    = np.mean(_ks)                   # prefix it with _ to avoid confusion
            _ke   = utils.sem(_ks)
            _l0   = np.mean(_l0s)
            _l0e  = utils.sem(_l0s)
            _r2   = calc_r2(pmfm, _pfit)
            _lb   = C['legends'][gk]
            _ky, _kye  = ky(_k, _l0, _ke, _l0e)

        # _txtx, _txty = [float(i) for i in pt_dd['text_coord']]
        # ax.text(_txtx, _txty, '\n'.join(['k   = {0:.1f} +/- {1:.1f} pN/nm'.format(_k, _ke),
        #                                  'l0  = {0:.1f} +/- {1:.2f} nm'.format(_l0, _l0e),
        #                                  'r^2 = {0:.2f}'.format(_r2),
        #                                  'ky  = {0:.1f} +/- {1:.1f} MPa'.format(_ky, _kye)]))

            ax.plot(bn, pmfm, color=C['colors'][gk], label=_lb)
            ax.fill_between(bn, pmfm-pmfe, pmfm+pmfe, 
                            where=None, facecolor=C['colors'][gk], alpha=.3)
            ax.plot(bn, _pfit, '--')
        decorate_ax(ax, pt_dd)

    else:
        col, row = utils.gen_rc(len(data.keys()))
        logger.info('col: {0}, row; {1}'.format(col, row))
        for k, gk in enumerate(data.keys()):
            ax = fig.add_subplot(row, col, k+1)
            # DIM of da: (x, 3, y), where x: # of replicas; y: # of bins
            da = data[gk]
            pre_pmfm = da.mean(axis=0)                  # means over x, DIM: (3, y)
            pre_pmfe = utils.sem3(da)                   # sems  over x, DIM: (3, y)

            if 'pmf_cutoff' in pt_dd:
                cf = float(pt_dd['pmf_cutoff'])
                bs, es = filter_pmf_data(pre_pmfm, cf)       # get slicing indices
            else:
                bs, es = filter_pmf_data(pre_pmfm)

            bn, pmfm, _ = sliceit(pre_pmfm, bs, es)             # bn: bin; pmfm: pmf mean
            bne, pmfe, _ = sliceit(pre_pmfe, bs, es)            # bne: bin err; pmfe: pmf err

            # pmf sem, equivalent to stats.sem(da, axis=0)
            pmfe = sliceit(pre_pmfe, bs, es)[1] # tricky: 1 corresponds err of pmf mean

            # now, prepare the errobars for the fit
            _pfits, _ks, _l0s = [], [], []
            for subda in da:
                sliced = sliceit(subda, bs, es)
                bn, pm, pe = sliced
                a, b, c = np.polyfit(bn, pm, deg=2)
                _pfv = parabola(bn, a, b, c)                    # pfv: pmf fit values
                _pfits.append(_pfv)
                _ks.append(convert_k(a))
                _l0s.append(-b/(2*a))

            _pfit = np.mean(_pfits, axis=0)
            _k    = np.mean(_ks)                   # prefix it with _ to avoid confusion
            _ke   = utils.sem(_ks)
            _l0   = np.mean(_l0s)
            _l0e  = utils.sem(_l0s)
            _r2   = calc_r2(pmfm, _pfit)
            _lb   = C['legends'][gk]
            _ky, _kye  = ky(_k, _l0, _ke, _l0e)

            _txtx, _txty = [float(i) for i in pt_dd['text_coord']]
            ax.text(_txtx, _txty, '\n'.join(['k   = {0:.1f} +/- {1:.1f} pN/nm'.format(_k, _ke),
                                             'l0  = {0:.1f} +/- {1:.2f} nm'.format(_l0, _l0e),
                                             'r^2 = {0:.2f}'.format(_r2),
                                             'ky  = {0:.1f} +/- {1:.1f} MPa'.format(_ky, _kye)]))

            ax.plot(bn, pmfm, label=_lb)
            ax.fill_between(bn, pmfm-pmfe, pmfm+pmfe, 
                            where=None, facecolor='blue', alpha=.3)
            ax.plot(bn, _pfit, '--')
            decorate_ax(ax, pt_dd)

    opf = A.output if A.output else os.path.join(
        C['data']['plots'], 
        '{0}.png'.format('_'.join([A.plot_type, A.analysis])))

    logger.info('saving to {0}'.format(opf))
    plt.savefig(opf)

def filter_pmf(pmf_data, cutoff=2.49):
    """
    try to determine the range of bin when prob_ave < cuttoff, which can be RT (~2.49 KJ/mol)
    return the beginning and ending slices;
    for vacuo, sometimes 2kt needed
    """
    # pdt: pmf_data_transposed, pmf_data should be a (3,n) multi-dimensional
    # array
    pdt = pmf_data.transpose()
    filtered = [d for d in pdt if d[1] < cutoff]
    return np.transpose(filtered)                           # tranpose back

def parabola(x, a, b, c):
    """return the array containing values: a * x^2 + b * x + c"""
    return  (a * x ** 2) + (b * x) + c

def calc_r2(values, fit_values):
    """calculate the correlation coefficients (R^2)"""
    ave = np.average(values)
    sst = sum((i - ave)**2 for i in values)
    ssreg = sum((i - ave)**2 for i in fit_values)
    r_square = float(ssreg) / sst
    return r_square

def convert_k(raw_k):
    # raw_k in KJ/(mol*nm^2)
    Nav= 6.023e23                                              # Avogadro constant
    k = float(raw_k) * 1e3 * 1e9 * 1e12  / Nav                       # unit: pN/nm
    return k

def ky(k, l0, ke=None, l0e=None, cuboid=True):
    """ky calculates the Young Modulus based on my model"""
    # e: means error, used for error propagation
    if cuboid:
        const = (2/3.) ** (1/3.)
    else:
        const = 4

    ky = const * k / l0

    if ke is not None and l0e is not None:
        kye = np.sqrt((l0e/l0) ** 2 + (ke/k) ** 2) * ky
        kye = const * kye
        return ky, kye
    else:
        return ky

def filter_pmf_data(pmf_data, cutoff=2.49):
    """
    try to determine the range of bin when prob_ave < RT, which is
    return the beginning and ending slices
    about 2.49 KJ/mol
    """
    pdt = pmf_data.transpose()

    flag = 1                                                # used as a flag
    slices = []
    # label the data as 1 (wanted) or 0 (unwanted)
    for k, d in enumerate(pdt):
        if flag:
            if d[1] < cutoff:                          # pmf is the second item
                slices.append(k)
                flag = 0
        else:
            if d[1] >= cutoff:
                slices.append(k)
                flag = 1
    print slices
    if len(slices) == 0:
        res = [0, -1]
    elif len(slices) == 1:
        n = slices[0]
        if abs(n - len(pdt)) > len(pdt) / 2.:
            res = [n, -1]
        else:
            res = [0, n]
    elif len(slices) == 2:
        res = slices
    elif len(slices) > 2:
        ds = []
        for k, s in enumerate(slices):
            if k == 0:
                pass
            else:
                ds.append(slices[k] - slices[k-1])
        b = ds.index(max(ds))
        e = b + 1
        res = [slices[b], slices[e]]
    logger.info("beg slice: {0}, end slice: {1}".format(*res))
    return res
