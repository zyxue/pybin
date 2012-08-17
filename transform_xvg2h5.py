#! /usr/bin/env python

import os
import sys
import tables
from configobj import ConfigObj

from common_func import backup_file
import argparse_action as aa
from xvg2h5 import h5tables as h5t
from xvg2h5 import xvg

TABLES = h5t.DD.keys()

def main():
    """
    basically it verifies the options and conf_dict first, then loop_xvgs,
    passing whatever should be parsed, ugly code!!! aaaaaahhh....
    """
    args = parse_cmd()

    # Verify the iterms in args
    conf = args.conf
    if not os.path.exists(conf):
        raise IOError("{0} cannot found".format(conf))

    conf_dict = ConfigObj(conf)
    SEQS, CDTS, TMPS, NUMS = aa.get_sctn(args, conf_dict['systems'])

    h5filename = conf_dict['data']['h5filename']
    title      = conf_dict['data']['title']

    # About the property
    ppty = args.ppty
    p_conf = conf_dict['properties'][ppty]         # property configuration
    property_obj = h5t.Property(ppty)              # including table desc & schema

    try:
        ogd = p_conf['ogd']                    # contains xvg_name and table_name patterns
    except KeyError:
        print "#" * 20
        print '"ogd" not specified in {0} in {1}'.format(ppty, conf)
        print "#" * 20
        sys.exit(1)

    if not args.nobk:
        backup_file(h5filename) # later when this script matures, this step may not be necessary

    # Start dealing with the h5 file now
    h5file = tables.openFile(h5filename, mode="a", title=title)
    filters = tables.Filters(complevel=8, complib='zlib')

    # zx_create_group is redundant and ugly code, I amd looking for a way to
    # overwrite creatGroup in table.file.File 2012-03-16
    ppty_group = zx_create_group(h5file, '/', ppty, filters=filters, title=property_obj.desc)   # property group
    ogd_group = zx_create_group(h5file, ppty_group._v_pathname, 'ogd', filters)
    ogd_path = ogd_group._v_pathname # should == ogd_path = os.path.join('/', ppty, 'ogd')

    # loop through xvg files and create a table for each one
    # ugly code!!! aaaaaahhh Should I learn loop? and make it more clear!
    # parsing so many args are really confusing
    loop_xvgs(SEQS, CDTS, TMPS, NUMS,
              ppty, h5file, property_obj, ogd, ogd_path
              )

def loop_xvgs(SEQS, CDTS, TMPS, NUMS,
              ppty, h5file, property_obj, ogd, ogd_path):
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
                        print "ATTENTION: {0} doesn't exist! YOU SURELY YOU KNOW THIS, RIGHT?".format(xvgf)
                    else:
                        tablename = ogd['tablename_pattern'].format(**locals())
                        tablepath = os.path.join(ogd_path, tablename)
                        if not h5file.__contains__(tablepath):
                            # unless the target table does not exist, then process the xvg_obj
                            xvg_obj = xvg.Xvg(xvgf)
                            table = h5file.createTable(ogd_path, tablename, property_obj.schema, xvg_obj.desc)
                            table.append(xvg_obj.data)
                            print "{0} IS TRANSFORMED to {1}".format(xvg_obj.filename, h5file.filename)
                        else:
                            table = h5file.getNode(tablepath)
                            # table.name is actually the same as tablename,
                            # using it remove the red line created by pyflake
                            print "{0} ALREADY EXIST in {1}".format(os.path.join(ogd_path, table.name), h5file.filename)


def zx_create_group(h5file, path, name, filters, title=''):
    if isinstance(path, str):
        pathname = os.path.join(path, name)
    if not h5file.__contains__(pathname):
        g = h5file.createGroup(path, name, title, filters)
    else:
        g = h5file.getNode(path, name)
    return g

def zx_create_table(h5file, grouppath, tablename, xvg_obj, property_table):
    """This function is deprecated, commented codes are for future reference only"""

    # ugly code, reverse should be removed accordly
    # property_cols = property_table.columns.keys()           # get the column names(keys)
    # property_cols.reverse()

    # row = table.row
    # for row_values in data:
    #     for k, v in enumerate(property_cols):
    #         row[v] = row_values[k]
    #     row.append()
    # table.flush()
    return 

def parse_cmd(cmd=None):
    """parse_cmd"""

    parser = aa.my_basic_parser()

    parser.add_argument('-a', '--property-name', type=str, dest='ppty', required=True,
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
