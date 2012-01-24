import os

import tables
import numpy as np
from configobj import ConfigObj

"""link stuff to reduce duplication"""

def main(h5file):
    conf_dict = ConfigObj('.h5.conf')
    h5f = tables.openFile(h5file, 'a')

    SEQS = conf_dict['systems']['SEQS']
    CDTS = conf_dict['systems']['CDTS']
    NUMS = conf_dict['systems']['NUMS']

    g = h5f.getNode(os.path.join('/', 'unv', 'ogd'))
    tablename_pattern = '{seq}{cdt}300s{num}'

    for seq in SEQS:
        for cdt in CDTS:
            for num in NUMS:
                tablename = tablename_pattern.format(seq=seq, cdt=cdt, num=num)
                if g.__contains__(tablename):
                    pass
                else:
                    # same tablename
                    target_table = h5f.getNode(os.path.join('/', 'unvp', 'ogd', tablename))
                    t = h5f.createSoftLink(g, tablename, target_table)
    h5f.close()

if __name__ == "__main__":
    h5file = '../mono_meo.h5'
    main(h5file)
