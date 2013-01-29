import os

import matplotlib.pyplot as plt
import numpy as np

import utils
L = utils.L

def alx(data, A, C, **kw):
    print 'start plotting alx...'

    fig = plt.figure(figsize=(12,9))
    D = C['plot'][A.analysis][A.plot_type]

    if A.merge:
        ax = fig.add_subplot(111)
        for k, gk in enumerate(data.keys()):
            da = data[gk]
            # ax.errorbar(da[0], da[1], yerr=da[2], label=C['legends'][gk])
            ax.plot(da[0], da[1], color=C['colors'][gk], label=C['legends'][gk])
            ax.fill_between(da[0], da[1]-da[2], da[1]+da[2], 
                            where=None, color=C['colors'][gk], alpha=.3)
        decorate_ax(ax, D)
    else:
        col, row = utils.gen_rc(len(data.keys()))
        L('col: {0}, row; {1}'.format(col, row))
        for k, gk in enumerate(data.keys()):
            ax = fig.add_subplot(row, col, k+1)
            da = data[gk]
            # ax.errorbar(da[0], da[1], yerr=da[2], label=C['legends'][gk])
            ax.plot(da[0], da[1], color=C['colors'][gk], label=C['legends'][gk])
            ax.fill_between(da[0], da[1]-da[2], da[1]+da[2], 
                            where=None, color=C['colors'][gk], alpha=.3)
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
