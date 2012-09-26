"""The following thing are for creating peptide in pymol, but I still haven't
figured out how to import pymol, apt usd python-2.6 while I am using
python-2.7."""

import os

def construct_cmd_for_peptide_creation(peptide_seq, pdb_outputfile, outputfile):
    opf = outputfile
    # add acetyl gropu
    opf.write("{0}\n".format("for aa in 'B': cmd._alt(string.lower(aa))"))
    # make the sequence
    opf.write("{0}\n".format("for aa in '{0}': cmd._alt(string.lower(aa))".format(peptide_seq)))
    # add the amine
    opf.write("{0}\n".format("editor.attach_amino_acid('pk1', 'nhh')"))
    # save the structure
    opf.write("{0}\n".format("save {0},((ace))").format(pdb_outputfile))
    # reinitialize
    opf.write("{0}\n".format("reinitialize"))

if __name__ == "__main__":
    seq_dd = {}

    # AA35
    # seq_dd.update(
    #     {
    #     '{0}35'.format(i) : i*35 for i in [
    #         'a', 'c', 'd', 'e', 'f', 
    #         'g', 'h', 'i', 'k', 'l', 
    #         'm', 'n', 'p', 'q', 'r', 
    #         's', 't', 'v', 'w', 'y',]
    #     }
    #     )

    # COMPLICATED SEQUENCES
    # seq_dd.update(
    #     {
    #         # not sure what this is, maybe ep2
    #         'ep2': ("FPGFGVGVGGIPGVAGVPGVGGVPGVGGVPGVGISPEAQAAAAAKAAKYGVGTPAAAAAKAAAKAAQFGLVPGVGVAPG"
    #                 "VGVAPGVGVAPGVGLAPGVGVAPGVGVAPGVGVAPGIGPEAQAAAAAKAAKYGVGTPAAAAAKAAAKAAQFGLVPGVGV"
    #                 "APGVGVAPGVGVAPGVGLAPGVGVAPGVGVAPGVGVAPGIGP"),
    #         }
    #     )

    # Aditi's SEQUENCES
    # seq_dd.update(
    #     {
    #         'gv9': "GV" * 18,
    #         "ga9": "GA" * 18,
    #         "a18": "A"  * 18,
    #         "ak2": "AAAAAAAKAAKAAAAAAA",
    #         "ayk": "AAAAAAAYAAAYAAAAAAA",
    #         },
    #     )
    
    # MY OWN SEQUENCES
    # seq_dd.update(
    #     {
    #         "sq1_gvpgv7": "GVPGV" * 7,
    #         }
    #     )

    # seq_dd.update(
    #     {
    #         # three sq1 combined, additional G is for later split
    #         "slsq1t003": "GVPGV" * 7 + "G" + "GVPGV" * 7 + "G" + "GVPGV" * 7,
        
    #         # 64 sq1 combined, verified to be correct with the original full sequence 2012-09-26
    #         "slsq1t064": ("GVPGV" * 7 + "G") * 63 + "GVPGV" * 7,
        
    #         # 128 sq1 combined, verified
    #         "slsq1t128": ("GVPGV" * 7 + "G") * 127 + "GVPGV" * 7,
    #         }
    #     )
    
    seq_dd.update(
        {
            "sq11_gp18":   "GP" * 18,
            "sq12_ggp12":  "GGP" * 12,
            "sq13_gggp9":  "GGGP" * 9,
            "sq14_ggggp7": "GGGGP" * 7,

            "sq15_pg18":   "PG" * 18,
            "sq16_ppg12":  "PPG"* 12,
            "sq17_pppg9":  "PPPG" * 9,
            "sq18_ppppg7": "PPPPG" * 7,
            }
        )
    
    outputfile = "___create_peptide.pml"
    with open(outputfile, 'w') as opf:
        for seq in sorted(seq_dd.keys()):
            pdb_outputfile = os.path.join("/home/zyxue/labwork/lala/", seq + '.pdb')
            construct_cmd_for_peptide_creation(seq_dd[seq], pdb_outputfile, opf)
