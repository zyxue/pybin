import re
import os

import tables
import numpy as np
from MDAnalysis import Universe

import utils
import objs
import prop

def transform(A, C, core_vars):
    h5 = utils.get_h5(C)

    if A.init_hdf5:
        init_hdf5(h5, core_vars)
        return 

    anal_dir = C['data']['analysis']

    for cv in core_vars:
        id_, path = cv['id_'], os.path.join('/', utils.get_dpp(cv))
        adir = os.path.join(anal_dir, 'r_{0}'.format(A.analysis)) # ad: anal dir, out of names
        if not os.path.exists(adir):
            raise IOError('{0}'.format("doesn't exist, please double check.".format(adir)))
        afile = os.path.join(adir, '{0}_{1}.{2}'.format(id_, A.analysis, A.filetype)) # af: anal file
        if not os.path.exists(afile):
            print "ATTENTION: {0} doesn't exist!".format(afile)
        else:
            tb_name = A.analysis
            tb_path = os.path.join(path, tb_name)
            if h5.__contains__(tb_path):
                tb = h5.getNode(tb_path)
                if not A.overwrite:
                    print "{0} ALREADY EXIST in {1}".format(os.path.join(path, tb.name), h5.filename)
                else:
                    tb.remove()
                    put_data(A.filetype, afile, 
                             prop.Property(A.analysis).schema,
                             h5, path, tb_name, cv)
                    print "{0} is overwritten with new data".format(tb_path)
            else:
                put_data(A.filetype, afile, 
                         prop.Property(A.analysis).schema,
                         h5, path, tb_name, cv)
                print "{0} IS TRANSFORMED to {1}".format(afile, tb_path)

def put_data(ft, f, schema, h5 ,path, tb_name, cv):
    if ft == 'xvg':
        fobj = objs.Xvg(f)
        tb = h5.createTable(where=path, name=tb_name, 
                            description=schema, 
                            title=fobj.desc)
        tb.append(fobj.data)
    elif ft == 'xpm':                                       # e.g. hbond map
        xpmf = f
        ndxf = f.replace('.xpm', '.ndx')
        dpp = utils.get_dpp(cv)
        io_files = utils.gen_io_files(dpp, cv['id_'])
        grof = io_files['ordergrof']
        flist = [xpmf, ndxf, grof]
        for i in flist:
            assert os.path.exists(i) == True
        hb_map = gen_hbond_map(*flist)                      # hb_map: hbond map
        tb = h5.createArray(where=path, name=tb_name, object=hb_map)
    return tb

def gen_hbond_map(xpm, ndx, grof):
    xpm = objs.XPM(xpm)
    hbndx = objs.HBNdx(ndx)

    univ = Universe(grof)
    pro_atoms = univ.selectAtoms('protein and not resname ACE and not resname NH2')
    hbonds_by_resid = hbndx.map_id2resid(pro_atoms)

    # pl: peptide length
    pl = pro_atoms.residues.numberOfResidues()

    hblist = []
    for i, j in zip(hbonds_by_resid, xpm.color_count):
        # -1 is because index in python starts from zero
        # j[1] is the probability of hbonds, which j[0] = 1 - j[1]
        hblist.append([i[0]-1, i[1]-1, j[1]])

    # +1: for missing resname ACE, such that it's easier to proceed in the next
    # step
    hb_map = np.zeros((pl+1, pl+1))
    for _ in hblist:
        hb_map[_[0]][_[1]] = _[2]

    return hb_map

def init_hdf5(h5, core_vars):
    """ init hdf5 if first time, make sure the directory hierarchy exists in hdf5 """
    filters = tables.Filters(complevel=8, complib='zlib')
    paths = []
    for cv in core_vars:
        PATH_KEY_RE = re.compile('path\d+')
        paths.append(sorted(
                [cv[p] for p in cv.keys() if re.match(PATH_KEY_RE, p)],
                key=lambda x: len(x)))

    for path in paths:
        for p in path:
            p = os.path.join('/', p)
            dirname = os.path.dirname(p)
            basename = os.path.basename(os.path.join('/', p))
            if not h5.__contains__(p):
                print 'creating... {0}'.format(p)
                h5.createGroup(where=dirname, name=basename, filters=filters)
