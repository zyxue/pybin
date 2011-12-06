import numpy as np

"""this is a xvg2png module"""

def xvg2array(xvgf):
    """This turns a xvg file into two array""" 
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

def xvg2array_data_points(xvgf):
    data_points = []
    with open(xvgf, 'r') as inf:
        for line in inf:
            if not line.startswith('#') and not line.startswith('@'):
                data_points.extend([float(i) for i in line.split()])
    return np.array(data_points)

if __name__ == "__main__":
    xvg2array_data_points('/home/zyxue/labwork/mono_su_as/r_connected_rg_equtrj/sq1e_connected_equtrj.xvg')
