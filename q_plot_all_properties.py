#!/usr/bin/env python
import matplotlib.pyplot as plt
from xvg2png import xvg2array_ap
import q_acc

"""quickly plot all properties in a single xvg file"""

def outline(options):
    infile = options.fs
    assert len(infile) == 1
    data = xvg2array_ap(infile[0])                          # infile is a list
    x = data.pop('time')       # pop the key of 'time' since it will consistent
                               # in all the subplots

    len_infs = len(data.keys())                         # time column has already been popped
    print data.keys()
    if options.overlap:
        overlap = options.overlap
        assert len_infs % overlap== 0, "the num of keys ({0}) are not even to do overlap ({1})".format(
            len_infs, overlap)
        row, col = q_acc.det_row_col(len_infs / overlap, options.morer)
    else:
        overlap = 1
        row, col = q_acc.det_row_col(len_infs, options.morer)

    fig = plt.figure(figsize=(24,11))
    # row, col = q_acc.det_row_col(len(data.keys()))

    for k, key in enumerate(data.keys()):
        if k % overlap == 0:
            ax = fig.add_subplot(row, col, k / overlap + 1)
            
        # ax = fig.add_subplot(row,col,k+1)
        print len(x), len(data[key]), key
        ax.plot(x, data[key], label=key)
        ax.set_title(key)
        ax.grid(b=True)
        # ax.set_ylim([-180, 180])

    q_acc.show_or_save(options.of)

if __name__ == '__main__':
    import time; b=time.time()
    outline(q_acc.parse_cmd())
    e = time.time()
    print "TIME ELAPSED: %f" % (e - b)
