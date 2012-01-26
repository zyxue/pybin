#! /usr/bin/env python

import argparse

class convert_seq(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) > 1:
            v = values
        else:
            vv = values[0]
            if '-' in vv:
                mi, ma = (int(i) for i in values[0].split('-'))
                v = [str(i) for i in xrange(mi, ma + 1)]
            else:
                v = values
        setattr(namespace, self.dest, ['sq{0}'.format(i) for i in v])

class convert_num(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) > 1:
            v = ['{0:02d}'.format(i) for i in (int(j) for j in values)]
        else:
            vv = values[0]
            if '-' in vv:
                mi, ma = (int(i) for i in vv.split('-'))
                v = ['{0:02d}'.format(i) for i in xrange(mi, ma + 1)]
            else:
                v = ['{0:02d}'.format(int(values[0]))]
        setattr(namespace, self.dest, v)

