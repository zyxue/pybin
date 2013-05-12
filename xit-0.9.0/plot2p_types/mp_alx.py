import re
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

import matplotlib.pyplot as plt

import utils

@utils.is_plot2p_type
def mp_alx(data, A, C, **kw):
    """alx for multiple properties (mp)"""
    pt_dd = utils.get_pt_dd(C, '_'.join(A.properties), A.plot2p_type)
    dsets = grp_datasets(data, pt_dd)

    fig = plt.figure(figsize=(12,9))
    if 'subplots_adjust' in pt_dd:
        fig.subplots_adjust(**utils.float_params(
                pt_dd['subplots_adjust'], 'hspace', 'wspace'))

    ncol, nrow = utils.gen_rc(len(dsets.keys()))
    logger.info('Chosen # of cols: {0}, # of rows; {1}'.format(ncol, nrow))
    for c, dsetk in enumerate(dsets.keys()):
        ax = fig.add_subplot(nrow, ncol, c+1)
        for prop_key in dsets[dsetk]:
            da = dsets[dsetk][prop_key]

            params = {}
            ax.plot(da[0], da[1], **params)
            ax.fill_between(da[0], da[1]-da[2], da[1]+da[2], 
                            where=None, facecolor=params.get('color'), alpha=.3)
        decorate_ax(ax, pt_dd, ncol, nrow, c)
    plt.savefig(utils.gen_output_filename(A, C))

def grp_datasets(data, pt_dd):
    grp_REs = pt_dd['grp_REs']
    dsets = OrderedDict()
    for c, RE in enumerate(grp_REs):
        for prop_key in data.keys():
            for sys_key in data[prop_key].keys():
                if sys_key not in dsets:
                    dsets[sys_key] = OrderedDict()
                if re.search(RE, prop_key):
                    dsets[sys_key][prop_key] = data[prop_key][sys_key]
    # dsets  = {
    #     'w300/sq1': {
    #         'rdf_c1vp': [array of x, array of y, array of ye],
    #         'rdf_c2vp': [array of x, array of y, array of ye],
    #         'rdf_c3vp': [array of x, array of y, array of ye],
    #         },
    #     'm300/sq1': {
    #         'rdf_c1vp': [array of x, array of y, array of ye],
    #         'rdf_c2vp': [array of x, array of y, array of ye],
    #         'rdf_c3vp': [array of x, array of y, array of ye],
    #         },
    #     }
    return dsets

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
        # ax.get_xaxis().set_visible(False)                   # this hide the whole axis
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
