import re
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

import matplotlib.pyplot as plt

import utils

def grp_datasets(data, pt_dd):
    grp_REs = pt_dd['grp_REs']
    dsets = OrderedDict()
    for c, RE in enumerate(grp_REs):
        dsetk = 'dset{0}'.format(c)                   # dsetk: dataset key 
        _ = dsets[dsetk] = {}
        _['data'] = OrderedDict()
        for key in data.keys():
            if re.search(RE, key):
                _['data'].update({key:data[key]})
        if 'texts' in pt_dd:
            _.update(text=pt_dd['texts'][c])
    return dsets

def grped_distr(data, A, C, **kw):
    """data: is an OrderedDict"""
    logger.info('start plotting {0} for {1}...'.format(A.plot_type, data.keys()))
    pt_dd = C['plots'][A.analysis]['grped_distr']
    dsets = grp_datasets(data,  pt_dd)

    fig = plt.figure(figsize=(12,9))
    if 'subplots_adjust' in pt_dd:
        fig.subplots_adjust(**utils.float_params(
                pt_dd['subplots_adjust'], 'hspace', 'wspace'))

    ncol, nrow = utils.gen_rc(len(dsets.keys()))
    logger.info('Chosen # of cols: {0}, # of rows; {1}'.format(ncol, nrow))
    for c, dsetk in enumerate(dsets.keys()):
        ax = fig.add_subplot(nrow, ncol, c+1)
        dset = dsets[dsetk]
        if 'text' in dset:
            ax.text(s=dset['text'], **utils.float_params(pt_dd['text'], 'x', 'y'))
        for kkey in dset['data']:                                 # ind: individual
            da = dset['data'][kkey]
            params = get_params(kkey, pt_dd)
            if A.plot_type ==  'grped_distr':
                ax.plot(da[0], da[1], **params)
                # facecolor uses the same color as ax.plot
                ax.fill_between(da[0], da[1]-da[2], da[1]+da[2], 
                                where=None, facecolor=params.get('color'), alpha=.3)
            elif A.plot_type == 'grped_distr_ave':
                # the data slicing can be confusing, refer to plot.py to see how to
                # data is structured
                ax.plot(da[0][0], da[0][1], **params)
                # facecolor uses the same color as ax.plot
                ax.fill_between(da[0][0], da[0][1]-da[0][2], da[0][1]+da[0][2], 
                                where=None, facecolor=params.get('color'), alpha=.3)

                # now, plot the vertical bar showing the average value
                m = da[1][0]                                    # mean
                e = da[1][1]                                    # error
                ax.plot([m,m], [0,1], color='black')
                ax.fill_betweenx([0,1], [m-e, m-e], [m+e, m+e],
                                 where=None, facecolor='black', alpha=.3)

        decorate_ax(ax, pt_dd, ncol, nrow, c)

    plt.savefig(utils.gen_output_filename(A, C))

def grped_distr_ave(data, A, C, **kw):
    """it's a variant of grped_distr by adding mean values in the distribution plot """
    grped_distr(data, A, C, **kw)

def get_params(key, pt_dd):
    params = {}
    if 'colors' in pt_dd:
        params['color'] = pt_dd['colors'][key]
    if 'legends' in pt_dd:
        params['label'] = pt_dd['legends'][key]
    else:
        params['label'] = key
    return params

def decorate_ax(ax, pt_dd, ncol, nrow, c):
    """c: counter"""
    ax.grid(which="major")
    if 'legends' in pt_dd:
        leg = ax.legend(loc='best')
    if 'xlim' in pt_dd: 
        ax.set_xlim(**utils.float_params(pt_dd['xlim'], 'left', 'right'))
    if 'ylim' in pt_dd:
        ax.set_ylim(**utils.float_params(pt_dd['ylim'], 'bottom', 'top'))

    if c < (ncol * nrow - ncol):
        ax.set_xticklabels([])
    else:
        if 'xlabel' in pt_dd: 
            ax.set_xlabel(**pt_dd['xlabel'])

    if c % ncol == 0:
        if 'ylabel' in pt_dd:
            ax.set_ylabel(**pt_dd['ylabel'])
    else:
        ax.set_yticklabels([])

    if 'xscale' in pt_dd: ax.set_xscale(pt_dd['xscale'])

    if 'legend_linewidth' in pt_dd:
        for l in leg.legendHandles:
            l.set_linewidth(float(pt_dd['legend_linewidth']))
