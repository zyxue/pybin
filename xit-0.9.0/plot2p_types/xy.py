import logging
logger = logging.getLogger(__name__)

import matplotlib.pyplot as plt

import utils

@utils.is_plot2p_type
def xy(data, A, C, **kw):
    """
    data structure of data, an OrderedDict
    data = {
        'x': {
            'groupkey0': [mean0,  std0],
            'groupkey1': [mean1,  std1],
            ...
            },
        'y': {
            'groupkey0': [mean0,  std0],
            'groupkey1': [mean1,  std1],
            ...
            }
        }
    """

    pt_dd = C['plots']['_'.join(A.analysis)][A.plot_type]
    xp, yp = A.analysis                                     # e.g. upup, unun
    xdata, ydata = data[xp], data[yp]

    denormx = [float(i) for i in pt_dd.get('denormx', [1] * len(xdata.keys()))]
    denormy = [float(i) for i in pt_dd.get('denormy', [1] * len(xdata.keys()))]

    # x, y means and errors
    xms, xes, yms, yes = [], [], [], []
    for c, key in enumerate(xdata.keys()):
        print key
        # xdata and ydata must have the same keys()
        xms.append(xdata[key][0] / denormx[c])
        xes.append(xdata[key][1] / denormx[c])
        yms.append(ydata[key][0] / denormy[c])
        yes.append(ydata[key][1] / denormy[c])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for xm, xe, ym, ye in zip(xms, xes, yms, yes):
        ax.errorbar(xm, ym, xerr=xe, yerr=ye)
    plt.savefig(utils.gen_output_filename(A, C))

def grp_datasets(data, pt_dd):
    grp_REs = pt_dd['grp_REs']
    print grp_REs

@utils.is_plot2p_type
def grped_xy(data, A, C, **kw):
    pt_dd = C['plots']['_'.join(A.analysis)][A.plot_type]
    grp_datasets(data, pt_dd)
