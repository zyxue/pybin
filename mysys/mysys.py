class Peptide(object):
    def __init__(self, psp): # psp: Peptide_Specific_Properties
        self.id = psp[0]
        self.seq = psp[1]
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
