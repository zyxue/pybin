import logging
logger = logging.getLogger(__name__)

import matplotlib.pyplot as plt
import numpy as np
from pprint import pformat

import utils

def simple_bar(grps, A, C, **kw):
    dd = C['plots'][A.analysis][A.plot_type]
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
    means = [i[0] for i in grps.values()]
    stds  = [i[1]  for i in grps.values()]

    if 'denorminators' in dd:
        denorms = [float(i) for i in dd['denorminators']]
        normalize = lambda x: [i/d for (i, d) in zip(x, denorms)]
        means = normalize(means)
        stds  = normalize(stds)

    # print xlocs, means, stds
    ax.bar(xlocs, means, bar_width, yerr=stds, color='white', hatch="\\")

    # decorate a bit
    ax.set_xlim((0 - 2 *space), (len(grps.items()) * (bar_width * type_of_bars + space) + space))
    ax.set_xticks(xlocs + bar_width/2.)                     # /2. to make it in the middle
    ax.set_xticks(xlocs + bar_width/2.)                     # /2. to make it in the middle
    ax.grid(which="major", axis='y')

    if 'ylim' in dd:
        ax.set_ylim(dd['ylim'])
    if 'xlabel' in dd: 
        ax.set_xlabel(dd['xlabel'])
    if 'ylabel' in dd: 
        ax.set_ylabel(dd['ylabel'], labelpad=10)
    if 'xticklabels' in dd:
        ax.set_xticklabels(dd['xticklabels'], rotation=15)
    else:
        ax.set_xticklabels(grps.keys(), rotation=20)
    if 'title' in dd:
        ax.set_title(dd['title'])
    if 'legend' in dd: 
        ax.legend(dd['legend'], loc='best')

    plt.savefig(utils.gen_output_filename(A, C))
    # if A.output:
    #     plt.savefig(A.output)
    # else:
    #     plt.savefig(os.path.join(
    #             C['data']['plots'], 
    #             '{0}.png'.format('_'.join([A.plot_type, A.analysis]))))

