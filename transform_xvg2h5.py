#! /usr/bin/env python

import os
import glob
import shutil
import argparse

import numpy as np
import tables
from configobj import ConfigObj

from argparse_action import convert_seq, convert_num
from xvg2h5 import h5tables as h5t
from xvg2h5 import xvg

TABLES = h5t.__tables__

def main():
    """
    basically it verifies the options and conf_dict first, then loop_xvgs,
    passing whatever should be parsed, ugly code!!! aaaaaahhh....
    """
    args = parse_cmd()

    # add try except for h5filename
    conf_dict = ConfigObj('.h5.conf')
    h5filename = conf_dict['data']['h5filename']
    title=conf_dict['data']['title']
    properties = conf_dict['properties']
    
    if not args.nobk:
        backup_file(h5filename) # later when this script matures, this step may not be necessary

    # Get the property name first, then based on it get the 
    # table description, table format
    pn = args.property_name
    if pn is None:
        raise ValueError('You must specify -p --property-name')
    elif not pn in properties:
        raise ValueError('"{0}" has not been included in the .h5.conf file'.format(pn))
    
    obj_property = h5t.Property(pn)
    p_conf = properties[pn]

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
              property_name, h5file, obj_property, ogd, ogdpath):
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

def parse_cmd():
    """parse_cmd"""
    parser = argparse.ArgumentParser(usage='transform data from xvg to h5')
    parser.add_argument('-s', dest='SEQS', nargs='+', action=convert_seq,
                        help="specify it this way, i.e. 1 3 4 or 1-9 (don't include 'sq')")
    parser.add_argument('-c', dest='CDTS', nargs='+',
                        help="specify it this way, i.e. w m o p e ")
    parser.add_argument('-t', dest='TMPS', default=None, nargs='+',
                        help='specify it this way, i.e "300 700", maybe improved later')
    parser.add_argument('-n', dest='NUMS', nargs='+', action=convert_num, required=True,
                        help='specify the replica number, i.e. 1 2 3 or 1-20')
    parser.add_argument('-p', '--property-name', type=str, dest='property_name', default=None,
                        help='you must specify the --property-name option from {0!r}'.format(TABLES))
    parser.add_argument('--nobk', dest='nobk', action='store_true', default=False,
                        help=('don\'t backup to save time, especially when the h5 file is big,'
                              'make sure your code works before using this option,'
                              'otherwise h5 file may be corrupted, and data lost'))
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
