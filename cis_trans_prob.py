#!/usr/bin/env python

import sys
from xvg2png import xvg2array

import numpy as np
# from scipy import integrate

# def integrate_prob(data, min_degree, max_degree):
#     """data should be a numpy array consisting pairs of [[angle1, prob1],
#     [angle2, prob2], [angle3, prob3], ... ]"""
#     probability = 0
#     for angle, prob in data:
#         if max_degree >= angle > min_degree:
#             probability += prob
#     return probability

def integrate_prob(data):
    """data should be a numpy array consisting pairs of [[angle1, prob1],
    [angle2, prob2], [angle3, prob3], ... ]"""
    probability = 0
    angle0, prob0 = data[0]
    for angle, prob in data[1:]:
        probability += (angle - angle0) * prob0
        angle0, prob0 = angle, prob
    return probability

def integrate_trans_prob(data):
    data1 = [d for d in data if -90 >= d[0] > -180]
    data2 = [d for d in data if 180 >= d[0] > 90]
    return integrate_prob(data1) + integrate_prob(data2)

def integrate_cis_prob(data):
    min_dg, max_dg = -90, 90
    data = [d for d in data if max_dg >= d[0] > min_dg]
    return integrate_prob(data)

def calc_dE(p_ratio, T):
    """p_ratio is the ratio of cisP to transP; T is the temperature"""
    R = 8.3144621e-3                                        # KJ/(K*mol)
    
    # deriving from the equ. p = exp-(dE/RT)
    dE = np.log(p_ratio) * R * T
    return dE

if __name__ == "__main__":
    infile, T = sys.argv[1:3]
    data = xvg2array(infile)
    # print sum(data[1])

    data = data.transpose()
    transP = integrate_trans_prob(data)
    cisP = integrate_cis_prob(data)
    print "trans probability: {0:8.3f}".format(transP)
    print "cis   probability: {0:8.3f}".format(cisP)
    print "TOTAL PROBABILITY: {0:8.3f}".format(transP + cisP)
    print

    p_ratio = cisP / transP
    print "P_cis / P_trans  : {0:8.3f}".format(p_ratio)
    dE = calc_dE(p_ratio, float(T))
    print "DeltaE (kJ/mol)  : {0:8.3f}".format(dE)
    print "DeltaE (kcal/mol): {0:8.3f}".format(dE * .239)
