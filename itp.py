#! /usr/bin/env python

"""This is script is incomplete, it's used to produce the itp file for opls,
given the input of all bonds"""

import copy

# bonds = [[1,2],                                             # hexanol
#          [1,3],
#          [1,4],
#          [1,5],
#          [5,6],
#          [5,7],
#          [5,8],
#          [8,9],
#          [8,10],
#          [8,11],
#          [11,12],
#          [11,13],
#          [11,14],
#          [14,15],
#          [14,16],
#          [14,17],
#          [17,18],
#          [17,19],
#          [17,20],
#          [20,21]]

bonds = [[1,2],                                             # hexanol
         [1,3],
         [1,4],
         [1,5],
         [5,6],
         [5,7],
         [5,8],
         [8,9],
         [8,10],
         [8,11],
         [11,12],
         [11,13],
         [11,14],
         [14,15],
         [14,16],
         [14,17],
         [17,18],
         [17,19],
         [17,20],
         [20,21],
         [20,22],
         [20,23],
         [23,24]]

def determine_dihedral(b1, b2, b3):
    rb1 = copy.copy(b1)
    rb2 = copy.copy(b2)
    rb3 = copy.copy(b3)

    rb1.reverse()
    rb2.reverse()
    rb3.reverse()

    for i in [b1, rb1]:
        for j in [b2, rb2]:
            for k in [b3, rb3]:
                if i[1] == j[0] and j[1] == k[0]:                
                    return i + k

dihedrals = []
for i, b1 in enumerate(bonds):
    for j, b2 in enumerate(bonds):
        for k, b3 in enumerate(bonds):
            if i < j < k:
                d = determine_dihedral(b1, b2, b3)
                if d:
                    dihedrals.append(d)

dihedrals.sort()
for d in dihedrals:
    print "{0:5d}{1:6d}{2:6d}{3:6d}{4:6d}".format(d[0], d[1], d[2], d[3], 3)
for d in dihedrals:
    print "{0:5d}{1:6d}{2:6d}".format(d[0], d[3], 1)
print len(dihedrals)


def determine_angle(b1, b2):
    rb1 = copy.copy(b1)
    rb2 = copy.copy(b2)
    
    rb1.reverse()
    rb2.reverse()

    for i in [b1, rb1]:
        for j in [b2, rb2]:
            if i[1] == j[0]:
                return i + [j[1]]

angles = []
for i, b1 in enumerate(bonds):
    for j, b2 in enumerate(bonds):
        if i < j:
            a = determine_angle(b1, b2)
            if a:
                angles.append(a)

for a in angles:
    print "{0:5d}{1:6d}{2:6d}{3:6d}".format(a[0], a[1], a[2], 3)
print len(angles)
