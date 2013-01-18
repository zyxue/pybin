import os

import matplotlib.pyplot as plt
import numpy as np

import utils

def alx(data, A, C, **kw):
    print 'start plotting alx...'

    fig = plt.figure(figsize=(12,9))
    col, row = utils.gen_rc(len(data.keys()))
    print 'col: {0}, row; {1}'.format(col, row)
    D = C['plot'][A.analysis][A.plot_type]
    for k, gk in enumerate(data.keys()):
        ax = fig.add_subplot(row, col, k+1)
        da = data[gk]
        ax.errorbar(da[0], da[1], yerr=da[2], label=C['legends'][gk])
        ax.legend(loc='best')
        ax.grid(which="major")
        if 'xlim' in D: ax.set_xlim([float(i) for i in D['xlim']])
        if 'ylim' in D: ax.set_ylim([float(i) for i in D['ylim']])
        if 'xlabel' in D: ax.set_xlabel(D['xlabel'])
        if 'ylabel' in D: ax.set_ylabel(D['ylabel'], labelpad=10)

        if 'xscale' in D: ax.set_xscale(D['xscale'])

    if A.output:
        plt.savefig(A.output)
    else:
        plt.savefig(os.path.join(
                C['data']['plots'], 
                '{0}.png'.format('_'.join([A.plot_type, A.analysis]))))
