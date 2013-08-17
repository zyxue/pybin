#!/usr/bin/env python

from collections import OrderedDict as odict
DD = odict()
src = [
    ('symb1', [33, 48]),
    ('num'  , [48, 58]),
    ('symb2', [58, 65]),
    ('upper', [65, 91]),
    ('symb3', [91, 97]),
    ('lower', [97, 123]),
    ('symb4', [123, 127]),
    ]
for _ in src:
    DD[_[0]] = _[1]

for k in DD.keys():
    print '{0:5s}:'.format(k.upper()),
    for j in range(*DD[k]):
        print '{0:2s}'.format(chr(j)),
    print 

