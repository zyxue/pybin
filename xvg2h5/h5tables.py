#! /usr/bin/env python

"""
everytime when adding a table, remember to add relevant info in
    __tables__
    class table_name(tables.IsDescription):
    d (in the Property class)

than modify the h5.conf in the directory you are working on
"""

import tables

__tables__ = ['e2ed', 'rg_c_alpha', 'sequence_spacing', 'dssp_E',
              'upup', 'upun', 'unun', 'upvp', 'upvn', 'unvn', 'unvp',
              'upv', 'unv',
              'rdf_upup', 'rdf_upun', 'rdf_unun',
              'rdf_upvp', 'rdf_upvn', 'rdf_unvp', 'rdf_unvn',
              'rama']

class e2ed(tables.IsDescription):
    """
    end-to-end distance data along the time trjectory
    VERY STRANGE: docstring doesn't work for subclass of tables.IsDescription 2012-12-13
    """
    time = tables.Float32Col(pos=0)
    e2ed = tables.Float32Col(pos=1)

class rama(tables.IsDescription):
    """
    phi, psi: dihedral angles
    aa: amino acid
    """
    phi = tables.Float32Col(pos=0)
    psi = tables.Float32Col(pos=1)
    # For types with a non-fixed size, this sets the size in bytes of individual items in the column.
    aa  = tables.StringCol(itemsize=10, pos=2)

class rg_c_alpha(tables.IsDescription):
    """
    Radius of gyration of C alpha along the time trjectory
    """
    time = tables.Float32Col(pos=0)
    rg_c_alpha = tables.Float32Col(pos=1)
    rg_c_alpha_x = tables.Float32Col(pos=2)
    rg_c_alpha_y = tables.Float32Col(pos=3)
    rg_c_alpha_z = tables.Float32Col(pos=4)

class dssp_E(tables.IsDescription):
    """
    dssp analysis, 
    E: extended conformation
    H: alpha helix
    T: turn
    B: isolated bridge
    G: 3-10 helix
    I: pi helix
    C: coil
    """
    time = tables.Float32Col(pos=0)
    Structure = tables.UInt32Col(pos=1)
    # number of structure types vary, which is a headache!
    # Coil = tables.UInt32Col(pos=2)
    # b-sheet = tables.Float32Col(pos=3)
    # rg_c_alpha_z = tables.Float32Col(pos=4)

class sequence_spacing(tables.IsDescription):
    """
    sequence_spacing
    """
    dij = tables.UInt32Col(pos=0)
    ave_d = tables.Float32Col(pos=1)
    std_d = tables.Float32Col(pos=2)
    num_data_points = tables.UInt32Col(pos=3)

# itemsize : int
# For types with a non-fixed size, this sets the size in bytes of individual items in the column.
# shape : tuple
# Sets the shape of the column. An integer shape of N is equivalent to the tuple (N,).
# dflt :
# Sets the default value for the column.
# pos : int
# Sets the position of column in table. If unspecified, the position will be randomly selected.

class upup(tables.IsDescription):
    """upup along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upup = tables.UInt32Col(pos=1)
    num_within_0_35nm = tables.UInt32Col(pos=2)

class upun(tables.IsDescription):
    """upun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upun = tables.UInt32Col(pos=1)

class unun(tables.IsDescription):
    """unun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_unun = tables.UInt32Col(pos=1)

class upvp(tables.IsDescription):
    """upvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upvp = tables.UInt32Col(pos=1)
    num_upvp_within_0_35nm = tables.UInt32Col(pos=2)

class upvn(tables.IsDescription):
    """upvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_upvn = tables.UInt32Col(pos=1)

class unvn(tables.IsDescription):
    """unvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_unvn = tables.UInt32Col(pos=1)

class unvp(tables.IsDescription):
    """unvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    num_unvp = tables.UInt32Col(pos=1)

#################### upv unv ####################

class upv(tables.IsDescription):
    """upv along the time trajectory"""
    time = tables.Float32Col(pos=0)
    upv = tables.UInt32Col(pos=1)

class unv(tables.IsDescription):
    """unv along the time trajectory"""
    time = tables.Float32Col(pos=0)
    unv = tables.UInt32Col(pos=1)

#################### rdf ####################

class rdf_upup(tables.IsDescription):
    """rdf_upup along the time trajectory"""
    time = tables.Float32Col(pos=0)
    rdf_upup = tables.Float32Col(pos=1)

class rdf_upun(tables.IsDescription):
    """rdf_upun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    rdf_upun = tables.Float32Col(pos=1)

class rdf_unun(tables.IsDescription):
    """rdf_unun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    rdf_unun = tables.Float32Col(pos=1)

class rdf_upvp(tables.IsDescription):
    """rdf_upvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    rdf_upvp = tables.Float32Col(pos=1)

class rdf_upvn(tables.IsDescription):
    """rdf_upvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    rdf_upvn = tables.Float32Col(pos=1)

class rdf_unvp(tables.IsDescription):
    """rdf_unvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    rdf_unvp = tables.Float32Col(pos=1)

class rdf_unvn(tables.IsDescription):
    """rdf_unvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    rdf_unvn = tables.Float32Col(pos=1)

class Property(object):
    def __init__(self, property_name):
        """values of d contain two parts: the table class & its description"""
        d = {
            'e2ed' : (e2ed, "end-to-end distance data along the time trjectory"),
            'rg_c_alpha': (rg_c_alpha, "Radius of gyration of C alpha along the time trjectory"),
            'sequence_spacing': (sequence_spacing, 'sequence_spacing'),
            'dssp_E': (dssp_E, 'dssp_E (b-sheet)'),
            'rama': (rama, "dihedral angle distribution for each frame along the time trjectory"),
            'upup': (upup, 'upup (i.e. intramolecular hbond) along the time trajectory'),
            'upun': (upun, 'upun along the time trajectory'),
            'unun': (unun, 'unun along the time trajectory'),
            'upvp': (upvp, 'upvp (i.e. intermolecular hbond) along the time trajectory'),
            'upvn': (upvn, 'upvn along the time trajectory'),
            'unvn': (unvn, 'unvn along the time trajectory'),
            'unvp': (unvp, 'unvp along the time trajectory'),

            'upv':  (upv, 'upv along the time trajectory'),
            'unv':  (unv, 'unv along the time trajectory'),

            'rdf_upup': (rdf_upup, 'rdf_upup along the time trajectory'),
            'rdf_upun': (rdf_upun, 'rdf_upun along the time trajectory'),
            'rdf_unun': (rdf_unun, 'rdf_unun along the time trajectory'),
            'rdf_upvp': (rdf_upvp, 'rdf_upvp along the time trajectory'),
            'rdf_upvn': (rdf_upvn, 'rdf_upvn along the time trajectory'),
            'rdf_unvp': (rdf_unvp, 'rdf_unvp along the time trajectory'),
            'rdf_unvn': (rdf_unvn, 'rdf_unvn along the time trajectory')
            }
        self.desc = d[property_name][1]
        self.schema = d[property_name][0]

if __name__ == "__main__":
    a = e2ed
