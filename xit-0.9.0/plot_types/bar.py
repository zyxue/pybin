import os
import logging
logger = logging.getLogger(__name__)

import matplotlib.pyplot as plt
import numpy as np
from pprint import pformat


def simple_bar(grps, A, C, **kw):
    logger.debug('\n{0}'.format(pformat((dict(grps)))))
    bar_width = 1.
    type_of_bars = 1                 # i.e. w, m
    space = 0.35                     # space between neigbouring groups of bars

    # x coordinates for bars
    min_, max_ = 0, len(grps.items()) * (bar_width * type_of_bars + space)
    step  = bar_width * type_of_bars + space
    xlocs = np.arange(min_, max_, step)[:len(grps.items())]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    grps_keys  = grps.keys()
    means = [i[0] for i in grps.values()]
    sems  = [i[1]  for i in grps.values()]

    # custmization failed
    # dd  = C['plots']
    # try:
    #     colors_dd = dd['colors']
    #     key = colors_dd['fmt'].format(**kw)
    #     color = colors_dd[key]
    # except:
    #     color = 'white'                                     # an arbitrary default
    #     logger.exception('No ["plots"]["color"] section found in {0}, using default color: {0} instead'.format(
    #             C.filename, color))

    ddd = C['plots'][A.analysis][A.plot_type]
    # print xlocs, means, sems
    ax.bar(xlocs, means, bar_width, yerr=sems, color='white', hatch="\\")

    # decorate a bit
    ax.set_xlim((0 - 2 *space), (len(grps.items()) * (bar_width * type_of_bars + space) + space))
    ax.set_xticks(xlocs + bar_width/2.)                     # /2. to make it in the middle
    ax.set_xticks(xlocs + bar_width/2.)                     # /2. to make it in the middle
    ax.grid(which="major", axis='y')

    if 'ylim' in ddd:
        ax.set_ylim(ddd['ylim'])
    if 'xlabel' in ddd: 
        ax.set_xlabel(ddd['xlabel'])
    if 'ylabel' in ddd: 
        ax.set_ylabel(ddd['ylabel'], labelpad=10)
    if 'xticklabels' in ddd:
        ax.set_xticklabels(ddd['xticklabels'], rotation=15)
    else:
        ax.set_xticklabels(grps_keys, rotation=20)
    if 'title' in ddd:
        ax.set_title(ddd['title'])
    if 'legend' in ddd: 
        ax.legend(ddd['legend'], loc='best')

    if A.output:
        plt.savefig(A.output)
    else:
        plt.savefig(os.path.join(
                C['data']['plots'], 
                '{0}.png'.format('_'.join([A.plot_type, A.analysis]))))
