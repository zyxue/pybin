#!/usr/bin/env

from mysys import read_mysys

MYSYS = read_mysys.read()

def calc_ave_dd(seq, cdt):
    dd = {
        'rg_c_alpha': [1., 'rg'],
        'rg_whole_length': [1., 'rg'],
        'rg_backbone': [1., 'rg'],
        'e2ed': [1., 'e2ed'],
        }                            # ppty_name: [denominator, interested_col]

    if seq in MYSYS:
        dd.update(
            {                  
                'dssp_E': [float(MYSYS[seq].len), 'structure'],
                'dssp_H': [float(MYSYS[seq].len), 'structure'],
                'dssp_T': [float(MYSYS[seq].len), 'structure'],
                'dssp_G': [float(MYSYS[seq].len), 'structure'],
                'dssp_I': [float(MYSYS[seq].len), 'structure'],
                'dssp_B': [float(MYSYS[seq].len), 'structure'],
                'dssp_C': [float(MYSYS[seq].len), 'structure'],
                'dssp_S': [float(MYSYS[seq].len), 'structure'],
                'dssp_X': [float(MYSYS[seq].len), 'structure'],
                
                'upup'  : [float(MYSYS[seq].hbg), 'upup' ],

                # g_mindist_excl1 double counts the contact, so divided by 2
                'unun'  : [float(MYSYS[seq].scnpg * 2),'unun'],
                'upun'  : [1., 'upun'],
                'upvp'  : [float(MYSYS[seq].hbg), 'upvp' ],
                'upvn'  : [float(MYSYS[seq].hbg), 'upvn' ],
                'unvp'  : [float(MYSYS[seq].scnpg), 'unvp' ],
                'unvn'  : [float(MYSYS[seq].scnpg), 'unvn' ],
                }
            )
        
    seqcdt = seq + cdt
    if seqcdt in MYSYS:
        dd.update(
            {
                'upv' : [float(MYSYS[seqcdt].nm_upv), 'upv'], 
                'unv' : [float(MYSYS[seqcdt].nm_unv), 'unv'],
                }
            )
    return dd


def calc_alx_dd(seq):
    return {                         # ppty_name: [denominator, x_col, y_col]
        'rg_c_alpha' : [1, 'time', 'rg_c_alpha'],
        'dssp_E'     : [float(MYSYS[seq].len), 'time', 'structure'],
        'conf_entropy' : [1, 'time', 'entropy'],
        'e2ed' : [1, 'time', 'e2ed'],
        'pmf_e2ed' : [1, 'x', 'pmf'],
        'rg_c_alpha': [1., 'time', 'rg'],
        'seqspacing' : [1, 'dij', 'ave_d'],
        # 'rdf_upup': ['radius', 'rdf'],
        # 'rdf_upun': ['radius', 'rdf'],
        # 'rdf_unun': ['radius', 'rdf'],
        # 'rdf_upvp': ['radius', 'rdf'],
        # 'rdf_upvn': ['radius', 'rdf'],
        # 'rdf_unvp': ['radius', 'rdf'],
        # 'rdf_unvn': ['radius', 'rdf'],
        
        'rdf_un1vn': [1, 'radius', 'rdf'],
        'rdf_un2vn': [1, 'radius', 'rdf'],
        'rdf_un3vn': [1, 'radius', 'rdf'],
        'rdf_un1vp': [1, 'radius', 'rdf'],
        'rdf_un2vp': [1, 'radius', 'rdf'],
        'rdf_un3vp': [1, 'radius', 'rdf'],
        
        'rdf_c1vn': [1, 'radius', 'rdf'],
        'rdf_c2vn': [1, 'radius', 'rdf'],
        'rdf_c3vn': [1, 'radius', 'rdf'],
        'rdf_c1vp': [1, 'radius', 'rdf'],
        'rdf_c2vp': [1, 'radius', 'rdf'],
        'rdf_c3vp': [1, 'radius', 'rdf'],
        
        'rg_whole_length': [1., 'time', 'rg'],
        
        }
