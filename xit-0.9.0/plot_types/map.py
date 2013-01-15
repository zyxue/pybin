import os

import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.axes_grid1 import ImageGrid

import utils

def map_(data, A, C, **kw):
    print 'start plotting map'

    fig = plt.figure(figsize=(12,9))
    col, row = utils.gen_rc(len(data.keys()))
    col, row = row, col
    grid = ImageGrid(fig, 111, nrows_ncols = (row, col), 
                     axes_pad = 0.3, 
                     add_all=True, label_mode = "L")

    print 'col: {0}, row; {1}'.format(col, row)
    D = C['plot'][A.analysis][A.plot_type]
    normalize(data)
    max_ = get_max(data)
    for k, gk in enumerate(data.keys()):
        ax = grid[k]

        da = data[gk]
        im = ax.imshow(da, origin="lower", cmap="Oranges",      # cmap could also be Greys
                  vmin=0, vmax=1, interpolation="nearest")
        im.set_clim(0, max_)
        ax.grid()
        if 'x_label' in D: ax.set_xlabel(D['x_label'])
        if 'y_label' in D: ax.set_ylabel(D['y_label'])
        ax.set_title(C['legends'][gk])

    plt.colorbar(im, shrink=.5, orientation='vertical', anchor=(1.3, 0))
    if A.output:
        plt.savefig(A.output)
    else:
        plt.savefig(os.path.join(
                C['data']['plots'], 
                '{0}.png'.format('_'.join([A.plot_type, A.analysis]))))

def get_max(data):
    max_ = []
    for i in data:
        max_.append(data[i].max(axis=0).max())
    return max(max_)
                    

def normalize(data):
    for i in data:
        data[i] = data[i] / np.sum(data[i])
