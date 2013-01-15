import os

import matplotlib.pyplot as plt
import numpy as np


def simple_bar(grps, A, C, **kw):
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
    sems  = [i[1]  for i in grps.values()]

    D = C['plot'][A.analysis][A.plot_type]
    print xlocs, means, sems
    ax.bar(xlocs, means, bar_width, yerr=sems, color='white', hatch="\\")

    # decorate a bit
    ax.set_xlim((0 - 2 *space), (len(grps.items()) * (bar_width * type_of_bars + space) + space))
    ax.set_xticks(xlocs + bar_width/2.)                     # /2. to make it in the middle
    ax.grid(which="major", axis='y')

    if 'ylim' in D: ax.set_ylim(D['ylim'])
    if 'xlabel' in D: ax.set_xlabel(D['xlabel'])
    if 'ylabel' in D: ax.set_ylabel(D['ylabel'], labelpad=10)
    if 'xticklabels' in D: ax.set_xticklabels(D['xticklabels'])
    if 'title' in D: ax.set_title(D['title'])
    if 'legend' in D: ax.legend(D['legend'], loc='best')

    if A.output:
        plt.savefig(A.output)
    else:
        plt.savefig(os.path.join(
                C['data']['plots'], 
                '{0}.png'.format('_'.join([A.plot_type, A.analysis]))))
