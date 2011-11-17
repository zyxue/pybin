#!/usr/bin/env python

import re
import fnmatch
import glob
import os
import sys
import numpy as np
from q_acc import parse_cmd
from xvg2png import xvg2array
from Mysys import read_mysys_dat


"""This script is highly customized"""

mysys = read_mysys_dat()

def try_mysorted(infs):
    if len(infs) == 6:                     # need improvement to verify the infs
        output = [ '' for i in range(6) ]
        template = re.compile('sq[1-6]')

        for inf in infs:
            sqx = template.search(inf).group()
            output[mysys[sqx].order] = inf
    else:
        output = infs
    return output

def pretty_output(change):
    print '{seq_id:8s}{seq:10s}{g_rg:5s}{g_rg_ste:5s}{upup:5s}{upup_ste:5s}{upun:5s}{upun_ste:5s}{unun:5s}{unun_ste:5s}{upvp:5s}{upvp_ste:5s}{unvp:5s}{unvp_ste:5s}'.format(
        seq_id='SEQ_ID',seq='Sequece',g_rg='Rg',g_rg_ste='ste',upup='upup',upup_ste='ste',upun='upun',upun_ste='ste',unun='unun',unun_ste='ste',upvp='upvp',upvp_ste='ste',unvp='unvp',unvp_ste='ste')

    for seq in try_mysorted(change.keys()):
        print '{seq_id:8s}{seq:10s}{g_rg:<5.0f}{g_rg_ste:<5.0f}{upup:<5.0f}{upup_ste:<5.0f}{upun:<5.0f}{upun_ste:<5.0f}{unun:<5.0f}{unun_ste:<5.0f}{upvp:<5.0f}{upvp_ste:<5.0f}{unvp:<5.0f}{unvp_ste:<5.0f}'.format(
            seq_id=mysys[seq].id, seq=mysys[seq].seq.strip(),
            g_rg=change[seq]['g_rg'][0]*100, g_rg_ste=change[seq]['g_rg'][1]*100,
            upup=change[seq]['upup'][0]*100, upup_ste=change[seq]['upup'][1]*100,
            upun=change[seq]['upun'][0]*100, upun_ste=change[seq]['upun'][1]*100,
            unun=change[seq]['unun'][0]*100, unun_ste=change[seq]['unun'][1]*100,
            upvp=change[seq]['upvp'][0]*100, upvp_ste=change[seq]['upvp'][1]*100,
            unvp=change[seq]['unvp'][0]*100, unvp_ste=change[seq]['unvp'][1]*100)

def error_change(a, sigma_a, b, sigma_b):
    """ a & b must be independent of each other """
    d = b - a
    sigma_b_a = np.sqrt(sigma_a**2 + sigma_b**2)                      # for the addition or subtraction
    sigma = np.sqrt(((sigma_b_a / float(d))**2 + (sigma_a / float(a))**2) * (d/float(a))**2) # for the division
    return sigma    

def quantify_ave_change(xf, yf, change):      # xf -> yf could be from water to methano
    t1 = re.compile('sq[0-9]')
    t2 = re.compile('g_rg|[uv][pn][uv][pn]?')
    xk1, yk1 = t1.search(xf).group(), t1.search(yf).group()
    xk2, yk2 = t2.search(xf).group(), t2.search(yf).group()
    assert xk1 == yk1, '{xk1} & {yk1} are different keys'.format(xk1=xk1, yk1=yk1)
    assert xk2 == yk2, '{xk2} & {yk2} are different keys'.format(xk2=xk2, yk2=yk2)
    k1, k2 = xk1, xk2

    xf_data, yf_data = xvg2array(xf)[1], xvg2array(yf)[1]
    
    (ave_xp, std_xp, ave_yp, std_yp) = (
        np.average(xf_data), np.std(xf_data), np.average(yf_data), np.std(yf_data))

    ave_change = (ave_yp-ave_xp) / ave_xp
    std_change = error_change(ave_xp, std_xp, ave_yp, std_yp)
    if not k1 in change.keys():
        change[k1] = {}
    change[k1][k2] = [ave_change, std_change]
    return change
    # print "%-30s%-10.2f%-30s%-10.2f%10.2f" % (xf, ave_xp, yf, ave_yp, (ave_yp-ave_xp)/ave_xp)n
    # return ave_xp, std_xp, ave_yp, std_yp

def outline(options):
    pwd = os.environ['PWD']
    dir_template = re.compile('g_rg|u[pn][u][pn]|u[pn]vp')
    dirs = [ d for d in os.listdir(pwd) if dir_template.search(d) and os.path.isdir(d) ]
    assert len(dirs) > 0
    xfs , yfs = [], []
    for d in dirs:
        xfs.extend(sorted(glob.glob(os.path.join(d, 'sq[1-6]w*'))))
        yfs.extend(sorted(glob.glob(os.path.join(d, 'sq[1-6]m*'))))
    assert len(xfs) == len(yfs), 'the number of files of xfs & yfs are not the same\n {0}\n {1}'.format(xfs, yfs)
    change = {}
    for xf, yf in zip(xfs,yfs):
        change = quantify_ave_change(xf,yf,change)
    pretty_output(change)

if __name__ == "__main__":
    outline(parse_cmd())
    # print error_change(1.3, 0.2, 0.9, 0.1)
