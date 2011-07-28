#!/usr/bin/env python

"""
This module will generate lists of hbond for varied usages from ndxfile grofile
xpmfile files, of which ndxfile & xpmfile could be generated from g_hbond with
-hbn -hbm options
"""

from Process_grofile import Process_grofile

def gen_hblist_index(ndxfile, target='[ hbonds_Protein ]'):
    flag = False                       # used to identify the boundary of target content
    hblist_index = []
    with open(ndxfile, 'r') as inf:
        for line in inf:
            if line.startswith('['):
                flag=True if line.startswith(target) else False; continue
            if flag:
                sl = line.strip().split()
                yield [int(sl[0]),int(sl[2])]
                # a list with sublist of [index_of_N, index_of_O]

def gen_hblist_resid(ndxfile,grofile):
    """replace index with resid in the hblist_index"""
    hb_resid = gen_hblist_index(ndxfile)
    g = Process_grofile(grofile)
    for hbpair in hb_resid:
        yield [g.resid(hbpair[0]), g.resid(hbpair[1])] 
        # a list with each sublist of [resid_of_N, resid_of_dCO]

def gen_hbmap_hblist(xpmfile,grofile,hbfile):
    """
    this hblist is generated to plot the hydrogen bond map(deprecated on 2011-04-04
    """
    hbmap_hblist = gen_hblist_resid(grofile, ndxfile)
    hbmap_hblist.reverse()      # so that we could use the xpm file upside down
    reversed_lines = reversed(open(xpmfile, 'r').readlines())
    for i, line in enumerate(reversed_lines):
        if line.startswith('"'):
            hbmap_hblist[i].append(line.count('o') / float(len(line)-4))
            # Now we need to count the number of "o" in each line of the matrix
            # 4 represents "",\n in a line
            # append the probablities of hbonds
        else:
            break
    return hbmap_hblist

def parse_xpm(xpmfile):
    for l in reversed(open(xpmfile, 'r').readlines()):
        if l.startswith('"'):
            ll = l.strip().replace('"','').replace(',','')
            yield ll   # remove "",\n in each line, and then append the whole
                       # line to hblist
        else:
            break

def gen_hblist(ndxfile,grofile,xpmfile):
    """
    Basically, this func is used to generature a dictionary with hbpair as keys,
    and a series of "o" as keys
    """
    hbpairs = list(gen_hblist_resid(ndxfile,grofile)) # hbl is agenerator object
    hbpairs.reverse()    # reverse it so that we could use the xpm file upside down,
                     # still cannot find a better way to parse this file other
                     # than reverse it on 2011-04-04
    os = list(parse_xpm(xpmfile))       # collection of the lines containing "o"
    assert len(hbpairs) == len(os), "%d VS %d: the number of hbpairs does equal that in xpmfile" % (len(hbl),len(os))
    for hbp, o in zip(hbpairs,os):
        hbp.append(o)
    return hbpairs
    # Now we have got the nested turn_hblist with each sublist
    # of ["resid_of N", "resid of CO", "the line with label "o" or space for every hbpair"]

if __name__ == "__main__":
    # import cProfile
    # cProfile.run("aa = gen_hb_map('/home/zyxue/labwork/monomers_su_v2/analysis_results_su_b20/hbppb20/original_data/aa.ndx','/home/zyxue/labwork/monomers_su_v2/analysis_results_su_b20/hbppb20/original_data/sq1.gro','/home/zyxue/labwork/monomers_su_v2/analysis_results_su_b20/hbppb20/original_data/sq1m300s00_hbm.xpm')")
    # for a in aa:
    #     print a[:2],len(a[2])
    print "this file should be used as a module"
