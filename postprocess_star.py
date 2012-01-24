import os

import tables
import numpy as np
from configobj import ConfigObj

from mysys import read_mysys

class tave_star(tables.IsDescription):
    """table ave"""
    pf = tables.StringCol(itemsize=15, pos=0)    # like an unique id                     
    ave_star = tables.Float32Col(pos=1)
    std_star = tables.Float32Col(pos=2)

# Modulize the code, and plot upup V.S. dssp_E

def main(h5file, pp, topproc):                              # pp: property
    mysys = read_mysys.read()
    conf_dict = ConfigObj('.h5.conf')

    h5f = tables.openFile(h5file, 'a')
    pp_path = h5f.getNode(os.path.join('/', pp))        # property_post_process

    if pp_path.__contains__(topproc):
        g = h5f.getNode(pp_path, topproc)
    else:
        g = h5f.createGroup(pp_path, topproc)
    print g

    SEQS = conf_dict['systems']['SEQS']
    CDTS = conf_dict['systems']['CDTS']
    NUMS = conf_dict['systems']['NUMS']
    tablename_pattern = conf_dict['postprocess'][topproc]['tablenamepattern']

    for seq in SEQS:
        for cdt in CDTS:
            print seq+cdt
            tablename = tablename_pattern.format(seq=seq, cdt=cdt)
            if g.__contains__(tablename):
                pass
            else:
                # prepare for creating a new table
                dd = {
                    'dssp_E': mysys[seq].len,
                    'upvp':mysys[seq+cdt].nm_upvp,
                    'upvn':mysys[seq+cdt].nm_upvn,
                    'unvp':mysys[seq+cdt].nm_unvp,
                    'unvn':mysys[seq+cdt].nm_unvn,
                    'upv': mysys[seq+cdt].nm_upv,
                    'unv': mysys[seq+cdt].nm_unv
                    }
                denorminator = dd[pp]
                try:
                    denorminator = float(denorminator)
                    pfpattern = conf_dict['postprocess'][topproc]['pfpattern']

                    aves = []
                    for num in NUMS:
                        pf = pfpattern.format(**locals())
                        t = h5f.getNode(os.path.join(pp_path._v_pathname, 'ogd'), pf)
                        if isinstance(t, tables.link.SoftLink):
                            print t.target
                            t = h5f.getNode(t.target)
                        # in order to ignore the varied name of columns
                        v = np.array(t.read().tolist())[:,1]
                        v_normed = v / denorminator
                        aves.append(
                            (pf, v_normed.mean(), v_normed.std()) # append a tuple
                            )
                    t = h5f.createTable(
                        g, tablename, tave_star,
                        title=\
                        'average value of each replica for {0} normded by {1}'\
                        .format(pp, denorminator))
                    t.append(aves)
                except ValueError:
                    print denorminator, seq+cdt, pp
    h5f.close()

if __name__ == "__main__":
    h5file = '../mono_meo.h5'
    topproc = 'ave_star'                        # type of postprocess. i.e. ave
    property = 'unvp'
    # Since it involves softlink, using rootUEP is not very convenient
    main(h5file, property, topproc)
