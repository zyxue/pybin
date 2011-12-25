#! /usr/bin/env python

def convert_seq(option, opt_str, value, parser):
    if not value is None:
        if '-' in value:
            mi, ma = value.split('-')                   # process args like "-s 1-9"
            range_ = [str(i) for i in range(int(mi), int(ma) + 1)]
        else:
            range_ = [i for i in value.split()]
        parser.values.SEQS = [ 'sq' + str(i) for i in range_]

def convert_cdt(option, opt_str, value, parser):
    if not value is None:
        # water, methanol, ethanol, propanol, octane, vacuo
        valid_cdts = ['w', 'm', 'e', 'p', 'o', 'v']
        split_v = value.split()
        for v in split_v:
            if v not in valid_cdts:
                raise ValueError('cdt {0:s} is not one of {1!r}'.format(v, valid_cdts))
        parser.values.CDTS = split_v

def convert_tmp(option, opt_str, value, parser):
    parser.values.TMPS = value.split()

def convert_num(option, opt_str, value, parser):
    if not value is None:
        if '-' in value:                   
            mi, ma = value.split('-')
            range_ = range(int(mi), int(ma) + 1)
        else:
            range_ = [int(i) for i in value.split()]
        parser.values.NUMS = [ '{0:02d}'.format(i) for i in range_]
