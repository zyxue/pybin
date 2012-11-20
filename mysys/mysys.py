import re

class Peptide(object):
    def __init__(self, psp): # psp: Peptide_Specific_Properties
        self.id = psp[0]
        self.seq = psp[1]
        self.seqstring = self.get_full_seq_string(psp[1])
        self.omega_list = self.create_omega_list(self.seqstring)

        self.color = psp[2]
        self.marker = psp[3]
        self.hbg = int(psp[4])
        self.scnpg = int(psp[5])
        self.gptg= float(psp[6])
        self.len= int(psp[7])
        self.tex_seq = psp[8]
        self.order = int(psp[9])
        self.natom = int(psp[10])
        self.seqitp = psp[11]
        self.KDhydropathy = psp[12]
        self.nPro = int(psp[13])

        self.n_x_pro = len(
            [                                    # number of X-Pro peptide bond
                omega for omega in self.omega_list if re.search('[A-Z]P[0-9]*',
                                                                omega)
                ]
            )
        self.n_non_x_pro = len(self.omega_list) - self.n_x_pro
    
    def get_full_seq_string(self, seq):
        # i.e. GVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGV
        seq = seq.upper()
        repeat, repeat_number = re.search('\(([A-Z]*)\)([0-9]*)', seq).groups()
        return repeat * int(repeat_number)

    def create_omega_list(self, seqstring):
        """
        this function creates a list of omega peptide bonds based on self.seq
        like ['GV01', 'VP02', ['PG03', ['GV04'], ['VG05'], ..., 'PG33',
        'GV34',]
        """
        lomega = []                                         # list of omega
        res1 = seqstring[0]
        if len(seqstring) < 100:         # that means less than 99 peptide bonds
            temp = "{0}{1}{2:02d}"      # template for formatting
        else:
            temp = "{0}{1}{2:03d}"
        for k, res2 in enumerate(seqstring[1:]):
            # using k+1, in order to make the naming consistent with that
            # produced by calc_omega.py in myg_tools/pybin.
            lomega.append(temp.format(res1, res2, k+1))
            res1 = res2                                 # moving forward
        return lomega
        
class Solvent(object):
    def __init__(self, ssp):                  # ssp: Solvent_Specific_Properties
        self.cdt = ssp[0]
        self.name = ssp[1]
        self.color = ssp[2]
        self.solgro = ssp[3]
        self.solitp = ssp[4]
        self.maxsol = ssp[5]
        self.box = ssp[6]
        self.solname =ssp[7]
        self.natom = int(ssp[8])

class Mono_sys(object):
    def __init__(self, monosp):                # monosp: mono_system Specific Propertis
        self.tid = monosp[0]
        self.nm_unvn = monosp[1]
        self.nm_unvp = monosp[2]
        self.nm_upvn = monosp[3]
        self.nm_upvp = monosp[4]
        self.nm_unv = monosp[5]
        self.nm_upv = monosp[6]
