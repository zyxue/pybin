#!/usr/bin/env python

import os
import sys

home = os.getenv('HOME')
def link(path):
    # path: e.g. xx/yy/pkg/include, pkg/include
    path = os.path.abspath(path)
    bn = os.path.basename(path)                             # bn: basename
    if bn == 'include':
        target_dir = os.path.join(home, 'zx_local/include')
        os.chdir(target_dir)
        for f in os.listdir(path):
            if f.endswith('.h'):
                relf = os.path.relpath(os.path.join(path, f))
                print relf
                os.symlink(relf, f)
        os.chdir(home)

    elif bn == 'lib':
        target_dir = os.path.join(home, 'zx_local/lib')
        os.chdir(target_dir)
        for f in os.listdir(path):            # f just contains a filename
            if f.startswith('lib'):
                relf = os.path.relpath(os.path.join(path, f))
                print relf
                os.symlink(relf, f)
        os.chdir(home)

    elif bn == 'bin':
        target_dir = os.path.join(home, 'zx_local/bin')
        os.chdir(target_dir)
        for f in os.listdir(path):            # f just contains a filename
            relf = os.path.relpath(os.path.join(path, f))
            print relf
            os.symlink(relf, f)
        os.chdir(home)
    else:
        print 'unrecognized path: {0}, exit..'.format(path)

if __name__ == "__main__":
    try:
        pkg_dir = sys.argv[1]
    except IndexError:
        print 'no pkg specified, exit..'
        sys.exit(-1)
        
    bin_dir = os.path.join(pkg_dir, 'bin')
    lib_dir = os.path.join(pkg_dir, 'lib')
    inc_dir = os.path.join(pkg_dir, 'include')

    flags = [(i, os.path.exists(i)) for i in [bin_dir, lib_dir, inc_dir]]
    for f in flags:
        print '####', f[0], f[1]
        if f[1]:
            link(f[0])
