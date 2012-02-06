#! /usr/bin/env python

# This is not ideal at all, The input in the command line should be all
# checked, if one is not in the mdp file, then warning should be printed to the
# screen


import os
import argparse


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, dest='infile',
                        help='mdp file')
    parser.add_argument('-p', type=str, dest='pp', nargs='+',
                        help='property')
    parser.add_argument('-v', type=str, dest='value', nargs='+',
                        help='value')
    args = parser.parse_args()
    return args

def main():
    args = parse_cmd()
    infile = args.infile
    infile_bk = os.path.join(os.path.dirname(infile),
                             'lala_' + os.path.basename(infile))

    pp2v = {                                                # property to value
        i: j for i, j in zip(args.pp, args.value)
        }

    if os.path.exists(infile):
        if not os.path.exists(infile_bk):
            os.rename(infile, infile_bk)
    else:
        if not os.path.exists(infile_bk):
            # both infile and infile_bk don't exist
            raise ValueError('both {0} & {1} do not exist'.format(infile, infile_bk))

    # to see if at least one provided propery name is found in the mdp file or not
    not_found_flag = True 
    with open(infile_bk) as inf:
        with open(infile, 'w') as opf:
            for line in inf:
                # property name in the mdp file
                pp_mdp = line.split('=')[0].strip()
                # if pp_mdp is found in the pp2v, then new_line_flag will be turned to red
                new_line_flag = False
                for pp in pp2v:
                    if pp == pp_mdp:
                        not_found_flag = False
                        new_line = '{0:25s}= {1}\n'.format(pp, pp2v[pp])
                        new_line_flag = True
                if new_line_flag:
                    opf.write(new_line)
                else:
                    opf.write(line)

    if not_found_flag:
        raise ValueError('{0} not in the {1}'.format(args.pp, infile))
    else:
        os.remove(infile_bk)

if __name__ == "__main__":
    main()
