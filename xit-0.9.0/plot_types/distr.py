import os

import numpy as np
import matplotlib.pyplot as plt

import utils
L = utils.L

def distr(data, A, C, **kw):
    L('start plotting distr...')

    fig = plt.figure(figsize=(12,9))
    D = C['plot'][A.analysis][A.plot_type]
    if A.merge:
        ax = fig.add_subplot(111)
        for k, gk in enumerate(data.keys()):
            da = data[gk]
            ax.errorbar(da[0], da[1], yerr=da[2], label=C['legends'][gk])
        decorate_ax(ax, D)
    else:
        col, row = utils.gen_rc(len(data.keys()))
        print 'col: {0}, row; {1}'.format(col, row)
        for k, gk in enumerate(data.keys()):
            ax = fig.add_subplot(row, col, k+1)
            da = data[gk]
            ax.errorbar(da[0], da[1], yerr=da[2], label=C['legends'][gk])
            decorate_ax(ax, D)

    opf = A.output if A.output else os.path.join(
        C['data']['plots'], 
        '{0}.png'.format('_'.join([A.plot_type, A.analysis])))

    L('saving to {0}'.format(opf))
    plt.savefig(opf)

def decorate_ax(ax, D):
    ax.legend(loc='best')
    ax.grid(which="major")
    if 'xlim' in D: ax.set_xlim([float(i) for i in D['xlim']])
    if 'ylim' in D: ax.set_ylim([float(i) for i in D['ylim']])
    if 'xlabel' in D: ax.set_xlabel(D['xlabel'])
    if 'ylabel' in D: ax.set_ylabel(D['ylabel'], labelpad=10)
    if 'xscale' in D: ax.set_xscale(D['xscale'])

def sliceit(l, b, e):
    l_t = l.transpose()          # (n,3) multi-dimensional data
    s_l = l_t[b:e].transpose()   # (3,n) multi-dimensional data
    return s_l

def pmf(data, A, C, **kw):
    L('start plotting pmf...')

    D = C['plot'][A.analysis][A.plot_type]

    fs = (float(i) for i in D['figsize']) if 'figsize' in D else (12,9)
    fig = plt.figure(figsize=fs)

    col, row = utils.gen_rc(len(data.keys()))
    L('col: {0}, row; {1}'.format(col, row))
    for k, gk in enumerate(data.keys()):
        ax = fig.add_subplot(row, col, k+1)
        # DIM of da: (x, 3, y), where x: # of replicas; y: # of bins
        da = data[gk]
        pre_pmfm = da.mean(axis=0)                  # means over x, DIM: (3, y)
        pre_pmfe = utils.sem3(da)                   # sems  over x, DIM: (3, y)

        if 'pmf_cuttoff' in D:
            cf = float(D['pmf_cuttoff'])
            bs, es = filter_pmf_data(pre_pmfm, cf)       # get slicing indices
        else:
            bs, es = filter_pmf_data(pre_pmfm)

        bn, pmfm, _ = sliceit(pre_pmfm, bs, es)
        bne, pmfe, _ = sliceit(pre_pmfe, bs, es)

        print bn, bne

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
        _k    = np.mean(_ks)                                   # prefix it with _ to avoid mess
        _ke    = utils.sem(_ks)                                   # prefix it with _ to avoid mess
        _l0   = np.mean(_l0s)
        _l0e  = utils.sem(_l0s)
        _r2   = calc_r2(pmfm, _pfit)
        _lb   = C['legends'][gk]
        _ky, _kye  = ky(_k, _l0, _ke, _l0e)

        _txtx, _txty = [float(i) for i in D['text_coord']]
        ax.text(_txtx, _txty, '\n'.join(['k   = {0:.1f} +/- {1:.1f} pN/nm'.format(_k, _ke),
                                         'l0  = {0:.1f} +/- {1:.1f} nm'.format(_l0, _l0e),
                                         'r^2 = {0:.2f}'.format(_r2),
                                         'ky  = {0:.1f} +/- {1:.1f} MPa'.format(_ky, _kye)]))

        ax.plot(bn, pmfm, label=_lb)
        ax.fill_between(bn, pmfm-pmfe, pmfm+pmfe, 
                        where=None, facecolor='blue', alpha=.3)
        ax.plot(bn, _pfit, '--')
        decorate_ax(ax, D)

    opf = A.output if A.output else os.path.join(
        C['data']['plots'], 
        '{0}.png'.format('_'.join([A.plot_type, A.analysis])))

    L('saving to {0}'.format(opf))
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
    for k, d in enumerate(pdt):
        if flag:
            if d[1] < cutoff:                          # pmf is the second item
                slices.append(k)
                flag = 0
        else:
            if d[1] >= cutoff:
                slices.append(k)
                flag = 1
    if len(slices) == 0:
        r = [0, -1]
    elif len(slices) == 1:
        n = slices[0]
        if abs(n - len(pdt)) > len(pdt) / 2.:
            r = [n, -1]
        else:
            r = [0, n]
    elif len(slices) == 2:
        r = slices
    elif len(slices) > 2:
        ds = []
        for k, s in enumerate(slices):
            if k == 0:
                pass
            else:
                ds.append(slices[k] - slices[k-1])
        b = ds.index(max(ds))
        e = b + 1
        r = [b, e]
    print "beg slice: {0}, end slice: {1}".format(*r)
    return r
