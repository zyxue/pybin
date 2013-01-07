#!/usr/bin/env python

import re
import numpy as np

class Xvg(object):
    def __init__(self, xvgf):
        self.filename = xvgf

    def fetch_data(self):
        """This fetches all the data contained in the xvg file (usually a
        multi-dimensional array)"""
        data = []
        f1 = open(self.filename, 'r')
        for line in f1:
            if line.startswith('#') or line.startswith('@') or 'nan' in line:
                pass
            else:
                sl = line.split()
                if len(sl) >= 2:
                    data.append([float(i) for i in sl])
        f1.close()
        data = np.array(data)
        return data

    def fetch_xy(self):
        # only returns the first two columns as x, y
        data = self.fetch_data()
        x = data[:, 0]
        y = data[:, 1]
        return np.array([x, y])

# The following 3 functions need further integration, with this object, the old
# xvg2png file is officially deprecated! 201210-05

    def xvg2array_eb(xvgf):
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
            data_points = [ float(line.split()[1]) for line in inf
                            if line[0] != '#' and line[0] != '@']
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
            match = re.match('@ s\d+ legend \".*"', line)
            if match:
                legends.append(match.group(0).split()[-1].strip('"'))
            elif not line.startswith('#') and not line.startswith('@'):
                data.append([float(i) for i in line.split()])
        inf.close()
        data = np.array(data)
        print data.shape[-1]
        if len(legends) != data.shape[-1]:
            raise ValueError("Check the integrity of {0},\n, the #{1} of legends doesn't match #{2} of data columns".format(xvgf, len(legends), data.shape[-1]))
        else:
            data_by_columns = {}
            for k, legend in enumerate(legends):
                data_by_columns[legend] = data[::, k]
        return data_by_columns
