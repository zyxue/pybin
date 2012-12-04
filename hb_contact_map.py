#!/usr/bin/env python

import numpy as np
from MDAnalysis import Universe

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

class XPM(object):
    def __init__(self, xpmf):
        # Open the xpm file for reading
        xpm = open(xpmf)
        
        # Read in lines until we fidn the start of the array
        meta = [xpm.readline()]
        while not meta[-1].startswith("static char *gromacs_xpm[]"):
            meta.append(xpm.readline())

        # The next line will contain the dimensions of the array
        dim = xpm.readline()

        # nx: width, ny: height, nc: # of colors, nb: # characters per pixel
        nx, ny, nc, nb = [int(i) for i in self._unquote(dim).split()]

        # The next dim[2] lines contain the color definitions
        # Each pixel is encoded by dim[3] bytes, and a comment
        # at the end of the line contains the corresponding value
        color_map = dict([self._col(xpm.readline()) for i in range(nc)])

        color_count = []
        for i in xpm:
            if i.startswith("/*"):                          # skip comment
                continue
            j = self._unquote(i)
            color_count.append([j.count(k)/float(nx) for k in sorted(color_map.keys())])

            # maybe calculate the number of one color and then do a
            # substraction would be faster, but as long as the file doesn't get
            # too big, count multiple times are acceptable
        xpm.close()

        self.file_name = xpmf
        self.color_map = color_map
        self.nx, self.ny, self.nc, self.nb = nx, ny, nc, nb
        self.color_count = color_count

    def _unquote(self, s):
        return s[1 + s.find('"'): s.rfind('"')]

    def _uncomment(self, s):
        return s[ 2 + s.find('/*'): s.rfind('*/')]

    def _col(self, c):
        color = c.split('/*')
        # value = unquote(color[1])
        symbol, color = self._unquote(color[0]).split('c')
        if symbol.strip():
            symbol = symbol.strip()
        else:                                # meaning symbol is made of space only
            symbol = " "
            # sys.stderr.write("%-40s: %s, %s, %s\n"%(c.strip(), symbol, color, value))
        return symbol, color

class HBNdx(object):
    def __init__(self, hb_ndx_file):
        ndxf = open(hb_ndx_file)

        for line in ndxf:
            if line.lstrip().startswith("["):
                ubline = self._unbracket(line)              # ubline: unbracketed line
                keyn = self._map_ubline(ubline)
                setattr(self, keyn, [])
                ref = getattr(self, keyn)
                flag = keyn
            else:
                sl = line.strip()
                if sl:
                    if flag == "sys":
                        ref.extend(int(i) for i in sl.split())
                    elif flag == "donors":
                        ref.append(int(sl.split()[0]))
                    elif flag == "acceptors":
                        ref.extend(int(i) for i in sl.split())
                    elif flag == "hbonds":
                        sls = sl.split()
                        ref.append([int(sls[0]), int(sls[-1])])

    def _map_ubline(self, ubline):
        dd = {
            'donors_hydrogens': 'donors',
            'acceptors': 'acceptors',
            'hbonds': 'hbonds'
            }
        for i in dd:
            if i in ubline:
                return dd[i]
        return "sys"                                    # meaning no useful key name found in dd

    def _unbracket(self, s):
        return s[1 + s.find('['): s.rfind(']')].strip()

    def map_id2resid(self, grof):
        hbonds_by_resid = []
        u = Universe(grof)
        for hb in self.hbonds:
            hbr = []
            for i in hb:
                # i-1 because u starts from 0 while ndx or gro file starts from 1
                hbr.append(u.atoms[i-1].resid)
            hbonds_by_resid.append(hbr)
        return hbonds_by_resid

def plot_contact_map(xpm, gro, ndx, outputfile):
    xpm = XPM(xpm)
    grof = gro
    hbndx = HBNdx(ndx)

    hbonds_by_resid = hbndx.map_id2resid(grof)

    gro_obj = Universe(grof)
    pl = len(gro_obj.residues)

    hblist = []
    for i, j in zip(hbonds_by_resid, xpm.color_count):
        i.append(j[1])                                      # 'o' mean hbond exists
        hblist.append(i)
    # hblist now is in the form of 
    # [resid_of N, resid of CO, probability_of_hbond, ]

    data = np.zeros((pl, pl))
    for sublist in hblist:
        data[sublist[0]][sublist[1]] = sublist[2]

    fig = plt.figure()
    grid = ImageGrid(fig, 111, nrows_ncols = (1, 1),
                     axes_pad = 0.3, add_all=True, label_mode = "L",
                     )

    ax = grid[0]
    im = ax.imshow(data, origin="lower", cmap="Paired",      # cmap could also be Greys
                   vmin=0, vmax=1, interpolation="nearest")

    ax.grid()
    ax.set_xlabel('C')
    ax.set_ylabel('N')
    plt.colorbar(im)

    plt.savefig(outputfile)


if __name__ == "__main__":
    xpm = 'sq1v0300s00_pro.xpm'
    gro = 'sq1v0300s00_pro.gro'
    ndx = 'sq1v0300s00_pro.ndx'

    plot_contact_map(xpm, gro, ndx, 'lala.pdf')
