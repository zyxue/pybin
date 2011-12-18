#! /usr/bin/env python

import tables

__tables__ = ['e2ed', 'rg_c_alpha']

class e2ed(tables.IsDescription):
    """
    end-to-end distance data along the time trjectory
    VERY STRANGE: docstring doesn't work for subclass of tables.IsDescription 2012-12-13
    """
    time = tables.Float32Col(pos=0)
    e2ed = tables.Float32Col(pos=1)
    e2ed_x = tables.Float32Col()
    e2ed_y = tables.Float32Col()
    e2ed_z = tables.Float32Col()

class rg_c_alpha(tables.IsDescription):
    """
    Radius of gyration of C alpha along the time trjectory
    """
    time = tables.Float32Col(pos=0)
    rg_c_alpha = tables.Float32Col(pos=1)
    rg_c_alpha_x = tables.Float32Col()
    rg_c_alpha_y = tables.Float32Col()
    rg_c_alpha_z = tables.Float32Col()

class upup(tables.IsDescription):
    """upup along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upup = tables.Float32Col(pos=1)
    num_upup_within_035nm = tables.Float32Col()

class upun(tables.IsDescription):
    """upun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upun = tables.Float32Col(pos=1)

class unun(tables.IsDescription):
    """unun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_unun = tables.Float32Col(pos=1)

class upvp(tables.IsDescription):
    """upvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upvp = tables.Float32Col(pos=1)
    num_upvp_within_035nm = tables.Float32Col()

class upvn(tables.IsDescription):
    """upvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upvn = tables.Float32Col(pos=1)

class unvn(tables.IsDescription):
    """unvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_unvn = tables.Float32Col(pos=1)

class unvp(tables.IsDescription):
    """unvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_unvp = tables.Float32Col(pos=1)

class Property(object):
    def __init__(self, property_name):
        d = {
            'e2ed' : (e2ed, "end-to-end distance data along the time trjectory"),
            'rg_c_alpha': (rg_c_alpha, "Radius of gyration of C alpha along the time trjectory"),
            'upup': (upup, 'upup (i.e. intramolecular hbond) along the time trajectory'),
            'upun': (upun, 'upun along the time trajectory'),
            'unun': (unun, 'unun along the time trajectory'),
            'upvp': (upvp, 'upvp (i.e. intermolecular hbond) along the time trajectory'),
            'upvn': (upvn, 'upvn along the time trajectory'),
            'unvn': (unvn, 'unvn along the time trajectory'),
            'unvp': (unvp, 'unvp along the time trajectory')
            }
        self.desc = d[property_name][1]
        self.schema = d[property_name][0]

if __name__ == "__main__":
    a = e2ed
