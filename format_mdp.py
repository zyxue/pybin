#!/usr/bin/env python

import shutil
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="inf", required=True)
args = parser.parse_args()

from common_func import backup_file
# The script will cause error if comment comtains "="
# But I won't debug now since it's enough for now for personal use

old_file = backup_file(args.inf)                                      # the returned backuped file

lines = []
with open(old_file) as inf:
    for line in inf:
        if not line.startswith(';') and line.strip():
            k, tropov = [i.strip() for i in line.split('=')]  # key, tropo_value
            if ';' in tropov:
                v, comv = tropov.split(';')         # comv: comment in the value
                v = v.split()
                comv = '; ' + comv.strip()
            else:
                comv = ' '
                v = tropov.split()
            v = ''.join(i.strip().ljust(15) for i in v)
            lines.append("{0:30s} = {1:30s}{2}\n".format(k, v, comv))
        else:
            lines.append(line)

with open(args.inf, 'w') as opf:
    opf.writelines(lines)
