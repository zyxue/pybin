#!/usr/bin/env python

import os
import sys
import argparse
import StringIO
import subprocess

def get_cpt_time(infile):
    proc = subprocess.Popen(['gmxcheck', '-f', infile],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        # It's strange that gromacs-4.[05].5 will direct out useful content as stderr
        for line in StringIO.StringIO(stderr):
            if 'Last frame' in line:
                sl = [i.strip() for i in line.split()]
                return_value = '{0:.5f}'.format(float(sl[-1]) / 1000)     # unit: ns
                return return_value
    else:
        if not os.path.exists(infile):
            return "{0} not exist".format(infile)
        else:
            return "{0} is corrupted".format(infile)

def get_tpr_time(tprfile):
    proc = subprocess.Popen(['gmxdump', '-s', tprfile],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if proc.returncode == 0:
        # Different from get_cpt_time, we use stdout this time
        nsteps_found_flag = False
        dt_found_flag = False
        for line in StringIO.StringIO(stdout):
            if 'nsteps' in line:
                nsteps = float(line.split('=')[1].strip())  # number of steps
                nsteps_found_flag = True
            elif "delta_t" in line:
                dt = float(line.split('=')[1].strip())      # unit: ps
                dt_found_flag = True

            if nsteps_found_flag and dt_found_flag:
                break
        result = "{0:.5f}".format(nsteps * dt / 1000)       # unit: ns
        return result
    else:
        if not os.path.exists(tprfile):
            return "{0} not exist".format(tprfile)
        else:
            return "{0} is corrupted".format(tprfile)

def parse_cmd():
    parser = argparse.ArgumentParser(
        prog='specify the gmxcheck version, and cpt file as input')
    parser.add_argument('-f', type=str, dest='inputfile', required=True,
                        help='specify the inputfile')
    args = parser.parse_args()
    return args

def main():
    args = parse_cmd()
    if args.inputfile[-3:] == "cpt":
        sys.stdout.write(get_cpt_time(args.inputfile))
    elif args.inputfile[-3:] == "tpr":
        sys.stdout.write(get_tpr_time(args.inputfile))
    else:
        sys.stderr.write("Unrecoganized file type\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
