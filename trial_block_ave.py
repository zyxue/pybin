#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from xvg2png import xvg2array

inf = '/home/zyxue/pyfiles/trial_block_ave.dat'
N = xvg2array(inf)[1]
print type(N), len(N)
len_N = len(N)

def ave_bi(bi, lb):
    assert len(bi) == lb, 'len(bi) = %d, lb = %d' % (len(bi), lb) 
    return np.average(bi)

# lbs = range(3, len_N / 2, 10)
# nbs = [ len_N / lb for lb in lbs ]                   # floor division

nbs = range(2, 5000, 100)
lbs = [ len_N / nb for nb in nbs ]

b_stds = []

for lb, nb in zip(lbs, nbs):
    b = lb
    sliced_data = N[0:(nb * lb + 1)]
    bs = [ sliced_data[i * b + 1 : i * b + b + 1] for i in range(0, nb) ] # all the blocks of data
    b_means = [ave_bi(bi, lb) for bi in bs ]                  # means of all the blocks
    assert len(b_means) == nb
    b_std = np.std(b_means)
    b_stds.append(b_std)

print len(lbs), len(b_stds)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(nbs, b_stds, 'o-')
plt.show()
