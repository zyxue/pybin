import numpy as np

def xvg2array(xvgf):
    f1 = open(xvgf, 'r')
    xlist = []
    ylist = []
    for line in f1:
        if line.startswith('#') or line.startswith('@'):
            pass
        else:
            linelist = line.split()
            if len(linelist) >= 2:
                xlist.append(eval(linelist[0]))
                ylist.append(eval(linelist[1]))
    xarray = np.array(xlist,dtype=float)
    yarray = np.array(ylist,dtype=float)
    f1.close()
    return xarray, yarray

def xvg2array_eb(xvgf, xvol, ycol):
    pass
