#! /usr/bin/env python


import sys
import os
import re
from configobj import ConfigObj

from mysys import read_mysys
from obj import Xvg
import argparse_action

def main():
    mysys = read_mysys.read()
    parser = argparse_action.my_basic_parser()
    parser.add_argument('-a', '--property-name', type=str, dest='ppty',
                        default="omega", help='default=omega')
    parser.add_argument('-g', dest='conf', default=".h5.conf",
                        help='specify the configuration file')
    args = parser.parse_args()

    conf = args.conf
    if not os.path.exists(conf):
        raise IOError("{0} cannot found".format(conf))

    conf_dict = ConfigObj(conf)
    SEQS, CDTS, TMPS, NUMS = argparse_action.get_sctn(args, conf_dict['systems'])

    for seq in SEQS:
        for cdt in CDTS:
            for tmp in TMPS:
                for num in NUMS:
                    # pf: prefix, passed along and used when writing the results
                    pf = conf_dict['dirchy']['prefix'].format(**locals())
                    xvgf = conf_dict['properties'][args.ppty]['ogd']['xvg_path_pattern'].format(**locals())
                    if not os.path.exists(xvgf):
                        print "{0} doesn't exist, YOU KONW THIS, RIGHT? ".format(xvgf)
                    else:
                        process(xvgf, mysys[seq], pf)
                        print "{0} is done".format(xvgf)

def process(xvgf, mysys_seq, pf):
    omega_list = mysys_seq.omega_list
    xvg_data = Xvg.Xvg(xvgf).fetch_data()

    if xvg_data.shape == (0,):
        raise ValueError("no data in {0}, please check.".format(xvgf))

    time = xvg_data[:, 0]
    # count number of frames from time.shape. Surely it can be obtained from
    # any element of omega_list, as well.
    nframes = time.shape[0] 
    omegas = xvg_data[:, 1:].transpose()

    # trans: 0,  cis: 1
    cis_x_pro = []
    cis_non_x_pro = []
    for oname, o  in zip(omega_list, omegas):
        match = re.search('[A-Z]P[0-9]*', oname)            # X-Pro
        if match:
            cis_x_pro.append(o.sum())
        else:
            cis_non_x_pro.append(o.sum())

    cis_non_x_pro_percent = sum(cis_non_x_pro) / float(mysys_seq.n_non_x_pro * nframes)
    if mysys_seq.n_x_pro:
        cis_x_pro_percent = sum(cis_x_pro) / float(mysys_seq.n_x_pro * nframes)
    else:
        cis_x_pro_percent = 0

    write_to_file(xvgf, cis_x_pro_percent, cis_non_x_pro_percent, pf)

def write_to_file(xvgf, cis_x_pro, cis_non_x_pro, pf):
    dirname = os.path.dirname(xvgf)
    basename = os.path.basename(xvgf)
    outputfile = os.path.join(dirname, '{0}.percent'.format(basename))
    with open(outputfile, 'w') as opf:
        opf.writelines('# {0:<20s}{1:<20s}{2:<20s}{3:<20s}{4:<20s}\n'.format(
                'replica_id', 
                'trans_x_pro', 'cis_x_pro',
                'trans_non_x_pro', 'cis_non_x_pro'))
                
        opf.writelines('  {0:<20s}{1:<20.5f}{2:<20.5f}{3:<20.5f}{4:<20.5f}\n'.format(
                pf, 
                1-cis_x_pro, cis_x_pro,
                1-cis_non_x_pro, cis_non_x_pro))

if __name__ == "__main__":
    main()
