#! /usr/bin/env python

import os
import sys
import glob
import shutil
import argparse

import numpy as np
import tables
from configobj import ConfigObj

from argparse_action import my_basic_parser, convert_seq, convert_num
from xvg2h5 import h5tables as h5t
from xvg2h5 import xvg

TABLES = h5t.__tables__

def main():
    """
    basically it verifies the options and conf_dict first, then loop_xvgs,
    passing whatever should be parsed, ugly code!!! aaaaaahhh....
    """
    args = parse_cmd()

    # check the validity of args
    if not os.path.exists(args.conf):
        raise IOError("Can not find {0}".format(args.conf))

    conf_dict = ConfigObj(args.conf)

    h5filename = args.h5f

    title=conf_dict['data']['title']
    properties = conf_dict['properties']
    
    if not args.nobk:
        backup_file(h5filename) # later when this script matures, this step may not be necessary

    # Get the property name first, then based on it get the 
    # table description, table format
    pn = args.ppty
    if pn is None:
        raise ValueError('You must specify -p --property-name')
    elif not pn in properties:
        raise ValueError('"{0}" has not been included in the .h5.conf file'.format(pn))
    
    obj_property = h5t.Property(pn)
    p_conf = properties[pn]                                 # property configuration

    h5file = tables.openFile(h5filename, mode="a", title=title)
    filters = tables.Filters(complevel=8, complib='zlib')

    pgrouppath = create_group(h5file, '/', pn, filters, title=obj_property.desc ) # property grouppath
    try:
        ogd = p_conf['ogd']
    except KeyError:
        print "#" * 20
        print "lala! Something is wrong! 'ogd' is not configured"
        print "#" * 20, "\n"

    create_group(h5file, os.path.join('/', pn), 'ogd', filters)
    ogdpath = os.path.join('/', pn, 'ogd')

    SEQS, CDTS, TMPS, NUMS = get_sctn(args, conf_dict['systems'])

    # name pattern for a table
    # loop through xvg files and create a table for each one
    # ugly code!!! aaaaaahhh Should I learn oop? and make it more clear!
    # parsing so many args are really confusing
    loop_xvgs(SEQS, CDTS, TMPS, NUMS,
              pn, h5file, obj_property, ogd, ogdpath
              )

def create_group(h5file, path, name, filters, title=''):
    if isinstance(path, str):
        pathname = os.path.join(path, name)
    if not h5file.__contains__(pathname):
        g = h5file.createGroup(path, name, title, filters)
    else:
        g = h5file.getNode(path, name)
    return g

def loop_xvgs(SEQS, CDTS, TMPS, NUMS,
              ppty, h5file, obj_property, ogd, ogdpath):
    """
    Under one group which is the name of the property, each xvg file will be
    transformed to a table, dirchy is not implemented, seems useless,
    unnecessary details.
    """
    for seq in SEQS:
        for cdt in CDTS:
            for tmp in TMPS:
                for num in NUMS:
                    xvgf = ogd['xvg_path_pattern'].format(**locals())
                    if not os.path.exists(xvgf):
                        print "ATTENTION: {0} doesn't exist! YOU SURE YOU KNOW THIS, RIGHT?".format(xvgf)
                    else:
                        print xvgf
                        objxvg = xvg.Xvg(xvgf)
                        tablename = ogd['tablename_pattern'].format(**locals())
                        create_table(h5file, ogdpath, tablename, objxvg.data, objxvg.desc, 
                                     obj_property.schema)

def create_table(h5file, grouppath, tablename, data, desc, property_table):
    # ugly code, reverse should be removed accordly
    property_cols = property_table.columns.keys()           # get the column names(keys)
    # property_cols.reverse()
    tablepath = os.path.join(grouppath, tablename)
    
    if not h5file.__contains__(tablepath):
        table = h5file.createTable(grouppath, tablename, property_table, title=desc)
        table.append(data)
        # row = table.row
        # for row_values in data:
        #     for k, v in enumerate(property_cols):
        #         row[v] = row_values[k]
        #     row.append()
        # table.flush()
    else:
        table = h5file.getNode(tablepath)
    return table

def get_sctn(args, configuration):
    SEQS = args.SEQS if args.SEQS else configuration['SEQS']
    CDTS = args.CDTS if args.CDTS else configuration['CDTS']
    TMPS = args.TMPS if args.TMPS else configuration['TMPS']
    NUMS = args.NUMS if args.NUMS else configuration['NUMS']
    return SEQS, CDTS, TMPS, NUMS

def backup_file(f):
    if os.path.exists(f):
        dirname = os.path.dirname(f)
        basename = os.path.basename(f)
        count = 1
        rn_to = os.path.join(
            dirname, '#' + basename + '.{0}#'.format(count))
        while os.path.exists(rn_to):
            count += 1
            rn_to = os.path.join(
                dirname, '#' + basename + '.{0}#'.format(count))
        shutil.copy(f, rn_to)

def parse_cmd(cmd=None):
    """parse_cmd"""

    parser = my_basic_parser()

    parser.add_argument('-f', dest='h5f', required=True,
                        help='specify the h5f file')
    parser.add_argument('-p', '--property-name', type=str, dest='ppty', required=True,
                        help='you must specify the --property-name option from {0!r}'.format(TABLES))

    parser.add_argument('-g', dest='conf', default=".h5.conf",
                        help='specify the configuration file')

    parser.add_argument('--nobk', dest='nobk', action='store_true', default=False,
                        help=('don\'t backup to save time, especially when the h5 file is big,'
                              'make sure your code works before using this option,'
                              'otherwise h5 file may be corrupted, and data lost'))
    if cmd is None:
        cmd = sys.argv[1:]

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    main()
