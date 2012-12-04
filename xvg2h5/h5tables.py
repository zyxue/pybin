#! /usr/bin/env python

"""
everytime when adding a table, remember to add relevant info in
    __tables__
    class table_name(tables.IsDescription):
    d (in the Property class)

than modify the h5.conf in the directory you are working on
"""

import tables

class e2ed(tables.IsDescription):
    """
    end-to-end distance data along the time trjectory
    VERY STRANGE: docstring doesn't work for subclass of tables.IsDescription 2012-12-13
    """
    time = tables.Float32Col(pos=0)
    e2ed = tables.Float32Col(pos=1)
    e2edx = tables.Float32Col(pos=2)
    e2edy = tables.Float32Col(pos=3)
    e2edz = tables.Float32Col(pos=4)

class rama(tables.IsDescription):
    """
    phi, psi: dihedral angles
    aa: amino acid
    """
    phi = tables.Float32Col(pos=0)
    psi = tables.Float32Col(pos=1)
    # For types with a non-fixed size, this sets the size in bytes of individual items in the column.
    aa  = tables.StringCol(itemsize=10, pos=2)

class rg(tables.IsDescription):
    """
    Radius of gyration of C alpha along the time trjectory
    """
    time = tables.Float32Col(pos=0)
    rg = tables.Float32Col(pos=1)
    rg_x = tables.Float32Col(pos=2)
    rg_y = tables.Float32Col(pos=3)
    rg_z = tables.Float32Col(pos=4)

class omega_percent(tables.IsDescription):
    """
    percentage of: cis trans peptide bonds
    """
    replica_id  = tables.StringCol(itemsize=10, pos=0)
    trans_x_pro = tables.Float32Col(pos=1)
    cis_x_pro = tables.Float32Col(pos=2)
    trans_y_x = tables.Float32Col(pos=3)
    cis_y_x = tables.Float32Col(pos=4)

class dssp(tables.IsDescription):
    """
    # This table must be redesigned and do_dssp program modified if you want to
    # do all secondary structure(ss) analysis, doing do_dssp for each ss is
    # unacceptable.

    dssp analysis, 
    E: extended conformation
    H: alpha helix
    T: turn
    B: isolated bridge
    G: 3-10 helix
    I: pi helix
    C: coil
    S: Bend (ono-hydrogen-bond based assignment)
    """
    time = tables.Float32Col(pos=0)
    structure = tables.UInt32Col(pos=1)
    # number of structure types vary, which is a headache!
    # Coil = tables.UInt32Col(pos=2)
    # b-sheet = tables.Float32Col(pos=3)
    # rg_z = tables.Float32Col(pos=4)

class seqspacing(tables.IsDescription):
    """
    sequence_spacing
    """
    dij = tables.UInt32Col(pos=0)
    ave_d = tables.Float32Col(pos=1)
    std_d = tables.Float32Col(pos=2)
    num_data_points = tables.UInt32Col(pos=3)

class pmf(tables.IsDescription):
    """potential of mean force"""
    x = tables.Float32Col(pos=0)
    pmf = tables.Float32Col(pos=1)

class entropy(tables.IsDescription):
    time = tables.Float32Col(pos=0)
    entropy = tables.Float32Col(pos=1)
    # number of structure types vary, which is a headache!
    # Coil = tables.UInt32Col(pos=2)
    # b-sheet = tables.Float32Col(pos=3)
    # rg_z = tables.Float32Col(pos=4)

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
    upup = tables.UInt32Col(pos=1)
    within_0_35nm = tables.UInt32Col(pos=2)

class upun(tables.IsDescription):
    """upun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    upun = tables.UInt32Col(pos=1)

class unun(tables.IsDescription):
    """unun along the time trajectory"""
    time = tables.Float32Col(pos=0)
    unun = tables.UInt32Col(pos=1)

class upvp(tables.IsDescription):
    """upvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    upvp = tables.UInt32Col(pos=1)
    upvp_within_0_35nm = tables.UInt32Col(pos=2)

class upvn(tables.IsDescription):
    """upvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    upvn = tables.UInt32Col(pos=1)

class unvn(tables.IsDescription):
    """unvn along the time trajectory"""
    time = tables.Float32Col(pos=0)
    unvn = tables.UInt32Col(pos=1)

class unvp(tables.IsDescription):
    """unvp along the time trajectory"""
    time = tables.Float32Col(pos=0)
    unvp = tables.UInt32Col(pos=1)

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

class rdf(tables.IsDescription):
    """rdf along the time trajectory"""
    radius = tables.Float32Col(pos=0)
    rdf = tables.Float32Col(pos=1)


DD = {
    'e2ed' : (e2ed, "end-to-end distance data along the time trjectory"),
    'rg_c_alpha': (rg, "Radius of gyration of C alpha along the time trjectory"),
    'rg_backbone': (rg, "Radius of gyration of C alpha along the time trjectory"),
    'rg_whole_length': (rg, "along the whole length of trjectory, usually used to determine the cutoff for collecting data"),
    'seqspacing': (seqspacing, 'sequence_spacing'),
    'pmf_e2ed': (pmf, 'potential_of_mean_force'),
    'omega_percent': (omega_percent, 'percentage of cis trans peptide bonds'),
    
    'dssp_E': (dssp, 'dssp_E (b-sheet)'),
    'dssp_H': (dssp, 'dssp_H (alpha-helix)'),
    'dssp_T': (dssp, 'dssp_T (hydrogen bonded turn)'),
    'dssp_G': (dssp, 'dssp_G (3-helix)'),
    'dssp_I': (dssp, 'dssp_I (5-helix)'),
    'dssp_B': (dssp, 'dssp_B (residue in isolated beta-bridge)'),
    'dssp_C': (dssp, 'dssp_C (coil)'),
    'dssp_S': (dssp, 'dssp_S (Bend)'),
    'dssp_X': (dssp, 'dssp_X (Bend)'),

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
    
    'rdf_upup': (rdf, 'rdf along the time trajectory'),
    'rdf_upun': (rdf, 'rdf along the time trajectory'),
    'rdf_unun': (rdf, 'rdf along the time trajectory'),
    'rdf_upvp': (rdf, 'rdf along the time trajectory'),
    'rdf_upvn': (rdf, 'rdf along the time trajectory'),
    'rdf_unvp': (rdf, 'rdf along the time trajectory'),
    'rdf_unvn': (rdf, 'rdf along the time trajectory'),
    
    'rdf_un1vn': (rdf, 'rdf along the time trajectory'),
    'rdf_un2vn': (rdf, 'rdf along the time trajectory'),
    'rdf_un3vn': (rdf, 'rdf along the time trajectory'),
    'rdf_un1vp': (rdf, 'rdf along the time trajectory'),
    'rdf_un2vp': (rdf, 'rdf along the time trajectory'),
    'rdf_un3vp': (rdf, 'rdf along the time trajectory'),
    
    'rdf_c1vn': (rdf, 'rdf along the time trajectory'),
    'rdf_c2vn': (rdf, 'rdf along the time trajectory'),
    'rdf_c3vn': (rdf, 'rdf along the time trajectory'),
    'rdf_c1vp': (rdf, 'rdf along the time trajectory'),
    'rdf_c2vp': (rdf, 'rdf along the time trajectory'),
    'rdf_c3vp': (rdf, 'rdf along the time trajectory'),
    
    'conf_entropy': (entropy, 'entropy with increasing sampling'),
    
    }

class Property(object):
    def __init__(self, property_name):
        """values of d contain two parts: the table class & its description"""
        self.desc = DD[property_name][1]
        self.schema = DD[property_name][0]

if __name__ == "__main__":
    a = e2ed
