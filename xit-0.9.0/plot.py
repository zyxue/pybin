import os
from collections import OrderedDict

import numpy as np

import objs
import prop
import utils

import plot_types as ptp

class UnrecoganizedPlotTypeError(Exception):
    pass

def plot(A, C, core_vars):
    h5 = utils.get_h5(C)
    pt_obj = prop.Property(A.analysis)
    grps = groupit(A, C, core_vars, h5)
    print "Groups: {0}".format(grps.keys())
    if A.plot_type == 'alx':
        data = OrderedDict()
        for gk in grps:
            path = os.path.join('/', gk)
            ar_name = '{0}_{1}'.format(A.plot_type, A.analysis) # array name
            ar_path = os.path.join(path, ar_name)
            if h5.__contains__(ar_path):
                if not A.overwrite:
                    data[gk] = h5.getNode(ar_path)
                    print 'Group: {0} fetched from previous result'.format(gk)
                else:
                    _ = h5.getNode(ar_path)
                    print 'overwriting {0}'.format(ar_path)
                    _.remove()
                    grp = grps[gk]
                    calc_alx(grp, pt_obj, data, gk, h5)
                    h5.createArray(where=path, name=ar_name, object=data[gk])
            else:
                grp = grps[gk]
                calc_alx(grp, pt_obj, data, gk, h5)
                h5.createArray(where=path, name=ar_name, object=data[gk])
                print 'Group: {0} is done'.format(gk)
        ptp.alx(data, A, C)
    elif A.plot_type == 'map':
        data = OrderedDict()
        for gk in grps:
            path = os.path.join('/', gk)
            ar_name = '{0}_{1}'.format(A.plot_type, A.analysis) # array name
            ar_path = os.path.join(path, ar_name)
            if h5.__contains__(ar_path):
                if not A.overwrite:
                    data[gk] = h5.getNode(ar_path)
                    print 'Group: {0} fetched from previous result'.format(gk)
                else:
                    _ = h5.getNode(ar_path)
                    print 'overwriting {0}'.format(ar_path)
                    _.remove()
                    ar = calc_map(grps, pt_obj, data, gk, h5)
                    data[gk] = h5.createArray(where=path, name=ar_name, object=ar)
            else:
                ar = calc_map(grps, pt_obj, data, gk, h5)
                data[gk] = h5.createArray(where=path, name=ar_name, object=ar)
        ptp.map_(data, A, C)

def calc_map(grps, pt_obj, data, gk, h5):
    grp = grps[gk]
    _l = []
    for tb in grp:                              # it could be array
        _l.append(tb)
    # no need to normalize when plotting a map!
    # norm  = pt_obj.norm('sq1') # dirty
    return np.array(_l).mean(axis=0)

def calc_alx(grp, pt_obj, data, gk, h5):
    _l = []
    ref_col = grp[0].read(field='time')
    for tb in grp:
        col1 = tb.read(field='time')
        assert (col1 == ref_col).all() == True
        col2 = tb.read(field=pt_obj.ifield)
        _l.append(col2)
    _a = np.array(_l)
    _aa = np.array([
            ref_col / 1000,                         # ps => ns
            _a.mean(axis=0),
            [utils.sem(_a[:,i]) for i in xrange(len(_a[0]))]])
    data[gk] = block_average(_aa)

def block_average(a, n=100):
    """a is a mutliple dimension array, n is the max number of data points desired"""
    if a.shape[1] < n:
        return a
    else:
        bs = int(a.shape[1] / n)                            # bs: block size
        print a.shape[1]
        if bs * n < a.shape[1] - 1:                         # -1 is math detail
            bs = bs + 1
        print 'block size: {0}, # of blocks: {1}'.format(bs, n)
        return np.array([a[:,bs*(i-1):bs*i].mean(axis=1) 
                         for i in xrange(1, n+1)]).transpose()

def groupit(A, C, core_vars, h5):
    print 'grouping...'
    grpid_key = A.grpid_key
    grps = OrderedDict()                                    # grped data
    for cv in core_vars:
        grpid = cv[grpid_key]
        if grpid not in grps:
            grps[grpid] = []
        path = os.path.join('/', utils.get_dpp(cv))
        tb = h5.getNode(path, A.analysis)
        grps[grpid].append(tb)
    return grps

# if A.plot_type in ['simple_bar']:
#             # e.g. A.norm: var2, cv[A.norm]: w, etc.
#             val = np.mean(values)
#         elif A.plot_type in ['alx']:
#             val = np.mean(values, axis=1)
            
#         if A.normid:                                        # normid; var1, var2, etc.
#             nm = pt_obj.norm(cv[A.normid])
#             grps[grpid].append(val / nm)
#         else:
#             grps[grpid].append(val)

#     for k in grps:
#         grps[k] = objs.Data(grps[k])

#     if A.plot_type == 'simple_bar':
#         ptp.simple_bar(grps, A, C)
#     if A.plot_type == 'alx':
#         ptp.alx(grps, A, C)
#     else:
#         raise UnrecoganizedPlotTypeError('{0} unrecoganized'.format(A.plot_type))
