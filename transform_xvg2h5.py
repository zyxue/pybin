#! /usr/bin/env python

import os
import glob
import shutil

import numpy as np
import tables

import callback
from configobj import ConfigObj
from optparse import OptionParser

from xvg2h5 import h5_tables as h5t

TABLES = h5t.__tables__

def main(OPTIONS):
    cfg_dict = ConfigObj('.h5.cfg')
    h5filename = cfg_dict['h5filename']
    backup_old_file(h5filename) # later when this script matures, this step may not be necessary

    if OPTIONS.property_name is None:
        raise ValueError('You must specify --property-name')
    
    ppty_name = OPTIONS.property_name

    ppty_desc = h5t.target_desc(ppty_name)
    ppty_table = h5t.target_table(ppty_name)
    ppty_cols = h5t.target_cols(ppty_name)

    xvg_pattchy_dict = cfg_dict['xvg_pattchy']
    xvg_pattern = os.path.join(xvg_pattchy_dict['xchy1'],
                               xvg_pattchy_dict['xchy2'])

    loop_xvgs(ppty_name, ppty_desc, ppty_table, ppty_cols, h5filename, cfg_dict, xvg_pattern)

def loop_xvgs(ppty_name, ppty_desc, ppty_table, ppty_cols, h5filename, cfg_dict, xvg_pattern):
    """
    Under one group which is the name of the property, each xvg file will be
    transformed to a table, dirchy is not implemented, seems useless,
    unnecessary details.
    """
    h5file = tables.openFile(h5filename, mode="a", title='all analysis results about v700_su')

    ppty_g = h5file.createGroup('/', ppty_name, title=ppty_desc)

    SEQS = options.SEQS if options.SEQS else cfg_dict['SEQS']
    CDTS = options.CDTS if options.CDTS else cfg_dict['CDTS']
    TMPS = options.TMPS if options.TMPS else cfg_dict['TMPS']
    NUMS = options.NUMS if options.NUMS else cfg_dict['NUMS']

    for seq in SEQS:
        for cdt in CDTS:
            for tmp in TMPS:
                for num in NUMS:
                    xvgf = xvg_pattern.format(**locals())
                    print xvgf
                    if os.path.exists(xvgf):
                        # parse the xvg file, get data and description
                        desc, data = parse_xvg(xvgf)

                        # create a table for each xvg file
                        tablename = cfg_dict['prefix'].format(**locals())
                        table = h5file.createTable(ppty_g, tablename, ppty_table, title=desc)
                        row = table.row
                        for row_values in data:
                            for k, v in enumerate(row_values):
                                row[ppty_cols[k]] = row_values[k]
                            row.append()
                        table.flush()

def backup_old_file(old_f):
    if os.path.exists(old_f):
        count = 1
        rn_to = '#' + old_f + '.{0}#'.format(count)                 # rename to
        while os.path.exists(rn_to):
            count += 1
            rn_to = '#' + old_f + '.{0}#'.format(count)                 # rename to
        shutil.copy(old_f, rn_to)

def parse_xvg(xvgf):
    """
    This function parses a xvg file, and returns a string of descripition & an
    multi dimensional matrix of data

    NOTE: Before modifing this script, please read carefully the format of you
    target xvg file, make sure it's backward compatible.  and create a new
    TABLE (i.e. class SomeProperty(tables.IsDescription) for the targeted
    property.
    """
    f1 = open(xvgf, 'r')
    desc = []
    data = []
    for line in f1:
        if line.startswith('#') or line.startswith('@'):
            desc.append(line)
        else:
            split_line = line.split()
            if len(split_line) >= 2:                        # Why do I need this line? I forgot
                data.append([float(i) for i in split_line])
    f1.close()
    desc = ''.join(desc)
    data = np.array(data)
    return desc, data

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
    (OPTIONS, args) = parser.parse_args()
    return OPTIONS

if __name__ == "__main__":
    options = parse_cmd()
    main(options)
