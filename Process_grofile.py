#!/usr/bin/env python
class Process_grofile:
    """
    process the grofile, retrieve content on Proteins only,
    no slovent content will be returned
    IMPORTANT: the number of atoms in protein must not exceed 9999
    Solvents that are taken into consideration in this script include
    MeO and SOL
    """
    def __init__(self,grofile):
        all_lines = open(grofile, 'r').readlines()
        del all_lines[:2]    # remove the first two lines in the grofile
        del all_lines[-1]    # remove the last line in the grofile
        lines = []           
        for k, line in enumerate(all_lines):
            if 'SOL' in line or 'MeO' in line:
                pass                           # remove the solvent lines
            else:
                lines.append(line.split())
        self.lines = lines
    def lines(self):
        return self.lines
    def pl(self):                       # return peptide length
        return int(self.lines[-1][0][:-3])
    def resid(self, real_index):
        return int(self.lines[real_index-1][0][:-3])
    def resname(self,real_index):
        return self.lines[real_index-1][0][-3:]
    def name(self,real_index):
        return self.lines[real_index-1][1]
    def index(self,real_index):
        return int(self.lines[real_index-1][2])
    # could be used for verification of this class
    def x(self,real_index):
        return self.lines[real_index-1][3]
    def y(self,real_index):
        return self.lines[real_index-1][4]
    def z(self,real_index):
        return self.lines[real_index-1][5]
    # ommit the velocities: no vx, vy, vx temporarily at 2011/01/03

def _verify():
    aa = Process_grofile('/home/zyxue/labwork/monomers_mp/mp_hbond/sq3m300_md_mp.gro')
    print aa.lines[0]
    print aa.pl()
    # print aa.resid(1)
    # print aa.resname(1)
    # print aa.name(1)
    # for i in range(1,100):
    #     print i, aa.index(i)
    # print aa.x(1)
    # print aa.y(1)
    # print aa.z(1)

if __name__ == '__main__':
    _verify()
