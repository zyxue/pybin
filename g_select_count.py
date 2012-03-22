#!/usr/bin/env python

import sys

infile = sys.argv[1]

f = open(infile)
count = {}
for line in f:
    if line[0] == '[':
        key = line.strip('[]\n ') 
        count[key] = []
    else:
        count[key].extend(line.split())

for k in count:
    print k, len(count[k])
