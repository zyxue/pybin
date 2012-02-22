import os
import numpy as np

def parse_xvg(xvgf, col=None):
    """
    This function parses a xvg file, and returns a string of descripition & an
    multi dimensional matrix of data

    NOTE: Before modifing this script, please read carefully the format of you
    target xvg file, make sure it's backward compatible.  and create a new
    TABLE (i.e. class SomeProperty(tables.IsDescription) for the targeted
    property.
    """
    f1 = open(xvgf, 'r')
    desc = []
    data = []
    for line in f1:
        if line.startswith('#') or line.startswith('@'):
            desc.append(line)
        else:
            split_line = line.split()
            if len(split_line) >= 2:                        # Why do I need this line? I forgot
                if col:
                    # added col before the number of results for some property
                    # like do_dssp_E varies for different trajectories, headache!
                    data.append(tuple(split_line[:col])) # tuple() necessary for table.append
                else:
                    data.append(tuple(split_line))
    f1.close()
    desc = ''.join(desc)
    return desc, data

class Xvg(object):
    def __init__(self, xvgf):
        self.xvgf = xvgf
        if 'dssp' in xvgf:
            desc, data = parse_xvg(xvgf, col=2)
        else:
            desc, data = parse_xvg(xvgf)
        self.desc = desc
        self.data = data

    def get_desc(self):
        """get the description (basically comments) of this xvgf"""
        return self.desc
    
    def get_data(self):
        """get the data contained (usually muti-dimensional array)"""
        return self.data

    def get_tablename(self, tn=None):
        """
        if tn is specified, tn will be used as the tablename, otherwise, the
        file name will be used
        """
        tablename = tn if tn else os.path.basename(self.xvgf)
        return tablename

