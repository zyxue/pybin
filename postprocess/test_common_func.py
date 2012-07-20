#! /usr/bin/env python

from util_func import parse_cmd
from argparse_action import convert_seq, convert_num

import unittest
# args = parse_cmd('-s 1 2 3')

class Test_parse_cmd(unittest.TestCase):
    def test_s_option(self):
        self.args = parse_cmd(['-s', '1', '2', '4', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.SEQS, ['sq1', 'sq2', 'sq4'])

        self.args = parse_cmd(['-s', '1-4', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.SEQS, ['sq1', 'sq2', 'sq3', 'sq4'])
        
        self.args = parse_cmd(['-s', '1-4', '39', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.SEQS, ['sq1', 'sq2', 'sq3', 'sq4', 'sq39'])

    def test_c_option(self):
        self.args = parse_cmd(['-c', 'w', 'm', 'e', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.CDTS, ['w', 'm', 'e'])

    def test_t_option(self):
        self.args = parse_cmd(['-t', '300', '700', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.TMPS, ['300', '700'])

    def test_n_option(self):
        self.args = parse_cmd(['-n', '1', '2', '10', '20', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.NUMS, ['01', '02', '10', '20'])
        
        self.args = parse_cmd(['-n', '1-4', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.NUMS, ['01', '02', '03', '04'])

        self.args = parse_cmd(['-n', '1-4', '10', '20', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.NUMS, ['01', '02', '03', '04', '10', '20'])

    def test_f_option(self):
        self.args = parse_cmd(['-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')


    def test_g_option(self):
        self.args = parse_cmd(['-g', 'test.conf', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

        self.assertEqual(self.args.conf, 'test.conf')

    def test_p_option(self):
        self.args = parse_cmd(['-p', 'test_property', '-p', 'test_property', '-f', 'test.h5'])
        self.assertEqual(self.args.h5f, 'test.h5')
        self.assertEqual(self.args.ppty, 'test_property')

if __name__ == "__main__":
    unittest.main()
