#! /usr/bin/env python

import re
import numpy as np

"""this is a xvg2png module"""

def xvg2array(xvgf):
    """This turns a xvg file into two array""" 
    data = []
    f1 = open(xvgf, 'r')
    for line in f1:
        if line.startswith('#') or line.startswith('@'):
            pass
        else:
            linelist = line.split()
            if len(linelist) >= 2:
                data.append([float(i) for i in linelist])
    f1.close()
    data = np.array(data)
    x = data[:, 0]
    y = data[:, 1]
    return x, y

def xvg2array_eb(xvgf, xvol, ycol):
    data = []
    f1 = open(xvgf, 'r')
    for line in f1:
        if line.startswith('#') or line.startswith('@'):
            pass
        else:
            linelist = line.split()
            if len(linelist) >= 2:
                data.append([float(i) for i in linelist])
    f1.close()
    data = np.array(data)
    x = data[:, 0]
    y = data[:, 1]
    e = data[:, 2]
    return x, y, e

def xvg2array_data_points(xvgf):
    data_points = []
    with open(xvgf, 'r') as inf:
        for line in inf:
            if not line.startswith('#') and not line.startswith('@'):
                data_points.extend([float(i) for i in line.split()])
    return np.array(data_points)

def xvg2array_ap(xvgf):
    """
    used when trying to plot all properties in the xvgf, sure the xvgf contains
    multiple properties.
    """
    legends = ['time']                   # time is not included in the xvg file
    data = []
    inf = open(xvgf, 'r')
    for line in inf:
        match = re.match('@ s\d legend \".*"', line)
        if match:
            legends.append(match.group(0).split()[-1].strip('"'))
        elif not line.startswith('#') and not line.startswith('@'):
            data.append([float(i) for i in line.split()])
    inf.close()
    data = np.array(data)
    if len(legends) != data.shape[-1]:
        raise "Check the integrity of {0},\n, the # of legends doesn't match # of data columns".format(xvgf)
    else:
        data_by_columns = {}
        for k, legend in enumerate(legends):
            data_by_columns[legend] = data[::, k]
    return data_by_columns

if __name__ == "__main__":
    xvg2array_ap('/home/zyxue/labwork/trial_md/trial_oco/energy.xvg')
