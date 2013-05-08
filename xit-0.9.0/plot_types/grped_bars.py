import re
import logging
logger = logging.getLogger(__name__)

import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

import utils

def grped_bars(grps, A, C, **kw):
    dd = C['plots'][A.analysis][A.plot_type]
    grp_REs = dd['grp_REs']
    new_grps = OrderedDict({}) # new_grps: meaning further grouping, based on which ploting
                  # will be done

    # structure of new_grps: dict of dict of dict ...
    # dataset = {
    #     'dataset0': {'data': [
    #             'groupkey0': ('mean0', 'std0'),
    #             'groupkey1': ('mean1', 'std1'),
    #             ...
    #             },
    #                  'color': 'red',
    #                  ...
    #                  },
    #     'dataset1': {'data': {
    #             'groupkey0': ('mean0', 'std0'),
    #             'groupkey1': ('mean1', 'std1'),
    #             ...
    #             },
    #                  'color': 'blue',
    #                  ...
    #                  },
    #     ...
    #     }
        
    for c, RE in enumerate(grp_REs):
        datasetk = 'dataset{0}'.format(c)                   # k means key
        _ = new_grps[datasetk] = {}
        _['data'] = OrderedDict()
        for key in grps.keys():
            if re.search(RE, key):
                _['data'].update({key:grps[key]})
        if 'colors' in dd:
            _.update(color=dd['colors'][c])
        if 'legends' in dd:
            _.update(legend=dd['legends'][c])

    bar_width = 1.
    type_of_bars = len(new_grps)   # i.e. w, m
    space = 0.35                     # space between neigbouring groups of bars  

    xlocs = np.arange(0, (len(grps) / type_of_bars) * (bar_width * type_of_bars + space),
                      bar_width * type_of_bars + space)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    rectss = []                                             # plural of rects
    for k, datasetk in enumerate(new_grps.keys()):
        dataset = new_grps[datasetk]
        means = [_[0] for _ in dataset['data'].values()]
        stds  = [_[1] for _ in dataset['data'].values()]
        if 'denorminators' in dd:
            denorms = [float(i) for i in dd['denorminators']]
            normalize = lambda x: [i/d for (i, d) in zip(x, denorms)]
            means = normalize(means)
            stds  = normalize(stds)
        rects = ax.bar(xlocs+(k * bar_width), means, bar_width, yerr=stds,
                       color=dataset.get('color'),
                      label=dataset.get('legend'))
        rectss.append(rects)

    ax.grid(which="major", axis='y')
    ax.set_xticks(xlocs + bar_width)

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.2f'%float(height),
                    ha='center', va='bottom')

    for rects in rectss:
        autolabel(rects)

    if 'ylim' in dd:
        ax.set_ylim(**utils.float_params(dd['ylim'], 'bottom', 'top'))
    if 'xlabel' in dd: 
        ax.set_xlabel(dd['xlabel'])
    if 'ylabel' in dd:
        ax.set_ylabel(**utils.float_params(dd['ylabel'], 'labelpad'))
    if 'xticklabels' in dd:
        ax.set_xticklabels(**dd['xticklabels'])
    if 'title' in dd:
        ax.set_title(dd['title'])
    if 'legends' in dd: 
        ax.legend(loc='best')

    plt.savefig(utils.gen_output_filename(A, C))
