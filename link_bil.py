#!/usr/bin/env python

import os
import sys
import argparse

home = os.getenv('HOME')

def link_or_unlink(relf, f, funlink=False):
    if funlink:
        if os.path.exists(f):
            print 'unlinking... {0}'.format(relf)
            os.unlink(f)
        else:
            print 'Not found {0}'.format(f)
    else:
        if not os.path.exists(f):
            print 'linking... {0}'.format(relf)
            os.symlink(relf, f)
        else:
            print 'already found {0} exiting.. please unlink first'.format(f)
            sys.exit(-1)

def link(path, funlink=False):
    # path: e.g. xx/yy/pkg/include, pkg/include
    path = os.path.abspath(path)
    bn = os.path.basename(path)                             # bn: basename
    if bn == 'include':
        target_dir = os.path.join(home, 'zx_local/include')
        os.chdir(target_dir)
        for f in os.listdir(path):
            if f.endswith('.h'):
                relf = os.path.relpath(os.path.join(path, f))
                link_or_unlink(relf, f, funlink)
        os.chdir(home)

    elif bn == 'lib':
        target_dir = os.path.join(home, 'zx_local/lib')
        os.chdir(target_dir)
        for f in os.listdir(path):            # f just contains a filename
            if f.startswith('lib'):
                relf = os.path.relpath(os.path.join(path, f))
                link_or_unlink(relf, f, funlink)
        os.chdir(home)

    elif bn == 'bin':
        target_dir = os.path.join(home, 'zx_local/bin')
        os.chdir(target_dir)
        for f in os.listdir(path):            # f just contains a filename
            relf = os.path.relpath(os.path.join(path, f))
            link_or_unlink(relf, f, funlink)
        os.chdir(home)
    else:
        print 'unrecognized path: {0}, exit..'.format(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='link or unlink newly installed package, mini pkg manager. just need to specify the dir')
    parser.add_argument('-l', type=str, dest='lpkg', help='link package')
    parser.add_argument('-u', type=str, dest='upkg', help='unlink package')
    parser.parse_args()
    args = parser.parse_args()
    if args.lpkg:
        funlink = False
        pkg_dir = args.lpkg
    elif args.upkg:
        funlink = True
        pkg_dir = args.upkg
    else:
        print 'No option specified, exit..'
        sys.exit(1)

    bin_dir = os.path.join(pkg_dir, 'bin')
    lib_dir = os.path.join(pkg_dir, 'lib')
    inc_dir = os.path.join(pkg_dir, 'include')

    flags = [(i, os.path.exists(i)) for i in [bin_dir, lib_dir, inc_dir]]
    for f in flags:
        print '####', f[0], f[1]
        if f[1]:
            link(f[0], funlink)
