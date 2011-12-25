#! /usr/bin/env python

import os
import glob
import shutil

import numpy as np
import tables

import callback
from configobj import ConfigObj
from optparse import OptionParser

from xvg2h5 import h5tables as h5t
from xvg2h5 import xvg

TABLES = h5t.__tables__

def main(options):
    """
    basically it verifies the options and conf_dict first, then loop_xvgs,
    passing whatever should be parsed, ugly code!!! aaaaaahhh....
    """
    conf_dict = ConfigObj('.h5.conf')
    h5filename = conf_dict['data']['h5filename']
    title=conf_dict['data']['title']
    properties = conf_dict['properties']
    backup_file(h5filename) # later when this script matures, this step may not be necessary

    # Get the property name first, then based on it get the 
    # table description, table format
    pn = options.property_name
    if pn is None:
        raise ValueError('You must specify --property-name')
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

    SEQS, CDTS, TMPS, NUMS = get_sctn(options, conf_dict['systems'])

    # name pattern for a table
    # loop through xvg files and create a table for each one
    # ugly code!!! aaaaaahhh Should I learn oop? and make it more clear!
    # parsing so many options are really confusing
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
                    if os.path.exists(xvgf):
                        print xvgf
                        objxvg = xvg.Xvg(xvgf)
                        tablename = ogd['tablename_pattern'].format(**locals())
                        create_table(h5file, ogdpath, tablename, objxvg.data, objxvg.desc, 
                                     obj_property.schema)
                    else:
                        print "{xvgf} doesn't exist.".format(xvgf=xvgf)

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

def get_sctn(options, configuration):
    SEQS = options.SEQS if options.SEQS else configuration['SEQS']
    CDTS = options.CDTS if options.CDTS else configuration['CDTS']
    TMPS = options.TMPS if options.TMPS else configuration['TMPS']
    NUMS = options.NUMS if options.NUMS else configuration['NUMS']
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
    parser = OptionParser(usage='transform data from xvg to h5"')
    parser.add_option('-p', '--property-name', type='str', dest='property_name', default=None,
                      help='you must specify the --property-name option from {0!r}'.format(TABLES))
    parser.add_option('-s', '--seq', type='str', dest='SEQS', default=None, 
                      action='callback', callback=callback.convert_seq,
                      help='specify it this way, i.e. "1 3 4" or "1-9"; don\'t include \'sq\''  )
    parser.add_option('-c', '--cdt', type='str', dest='CDTS', default=None, 
                      action='callback', callback=callback.convert_cdt,
                      help='specify it this way, i.e. "w m o p e"')
    parser.add_option('-t', '--tmp', type='str', dest='TMPS', default=None, 
                      action='callback', callback=callback.convert_tmp,
                      help='specify it this way, i.e "300 700", maybe improved later')
    parser.add_option('-n', '--num', type='str', dest='NUMS', default=None, 
                      action='callback', callback=callback.convert_num,
                      help='specify the replica number, i.e. "1 2 3" or "1-20"')
    (options, args) = parser.parse_args()
    return options

if __name__ == "__main__":
    options = parse_cmd()
    main(options)
