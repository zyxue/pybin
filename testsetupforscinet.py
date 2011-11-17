#!/usr/bin/python

"""
This module could help do similar test MDs with certain different varaibles,
usually it can do all the step before em, nvt, npt equilibration before qsub

To use this module, you need a ini/ directory which contains all the needed
.mdp files, a 0_mdrun.sh file which contains the bash code that needs to
be run after qsub

Variables you need to specify includes 
testdir, inidir, ntest, sqname0, sqname, dsize, wtrmodel, wtr_gro, bt
nodenum, jobname, walltime
"""

import os
import time

def sysconfig(sqname0='sq0',sqname='sqdefault',dsize=0.7,wtrmodel='tip4p',wtr_gro='tip4p.gro',bt='dodecahedron'):
    os.system("echo '5\n3\n3' | pdb2gmx -f %s -o %s_prd.gro -p %s.top -ter -water %s" %
              (sqname0, sqname, sqname, wtrmodel))
    os.system('editconf -f %s_prd.gro -o %s_nbx.gro -c -d %s -bt %s' %
              (sqname, sqname, dsize, bt))
    os.system('genbox -cp %s_nbx.gro -cs %s -p %s.top -o %s_wtr' % 
              (sqname, wtr_gro, sqname, sqname))

def do_testmd(testdir = './',
              inidir = './', # e.g. '/home/zyxue/labwork/%s_w300pv5/ini/'
              ntest = 2,
              sqname0 = 'sq0',
              sqname = 'sqdefault',
              dsize = 0.7,
              wtrmodel = 'tip4p',
              bt = 'dodecahedron'):
    
    """go to testdir & create a logfile"""
    os.chdir(testdir)
    logfile = open('%slogfile.log' % testdir, 'w')
    
    """loop: make sub test directories & copy files from inidir"""
    for i in range(1, ntest+1):
        testi = 'test%s' % i
        os.mkdir(testi)
        os.chdir(testi)
        os.system('cp -r %s* %s' % (inidir, testdir+testi))
        sysconfig(sqname0, sqname, dsize)
        dsize += .1
        # walltime = '48:00:00'
        # nodenum = '4:ib'
        # jobname = testi
        # walltime = '48:00:00'
        # os.system('qsub -l nodes=%s:ppn=8,walltime=%s,os=centos53computeA -N %s 0_mdrun.sh'
        #           % (nodenum, walltime, jobname))
        tt = time.localtime()
        logfile.write('dsize=%s qsub%s %s/%s/%s,%s:%s:%s\n'
                      % (str(dsize), testi, tt[0],tt[1],tt[2],tt[3],tt[4],tt[5]))
        os.chdir(testdir)

if __name__ == '__main__':
    print 'hello'
    os.system('rm -r test[1-6]')
    do_testmd(testdir = '/home/zyxue/labwork/trial_test1/',
              inidir = '/home/zyxue/labwork/ini/', # e.g. '/home/zyxue/labwork/%s_w300pv5/ini/'
              ntest=2,
              sqname0 = 'gvpgv5.pdb',
              sqname = 'sq1')

# os.system("echo '5\n3\n3' | pdb2gmx -f %s -o %s_prd.gro -p %s.top -ter -water tip4p")
# dsize = 0.1
# os.system('editconf -f %s_prd.gro -o %s_nbx.gro -c -d %s -bt dodecahedron' % dsize)
# os.system('genbox -cp %s_nbx.gro -cs tip4p.gro -p %s.top -o %s_wtr')

# EXE='/project/pomes/cneale/GPC/exe/intel/gromacs-4.0.5/exec/bin/mdrun_openmpi-1.4.1'
# MPIRUN = '/scinet/gpc/mpi/openmpi/1.4.1-intel-v11.0-ofed/bin/mpirun'

# os.system('grompp -v -f em.mdp -c %s_wtr.gro -p %s.top -o %s_em.tpr -po %s_em')
# os.system('%s -np 8 %s -v -deffnm %s_em' % (MPIRUN, EXE))

# os.system('grompp -v -f nvt.mdp -c %s_em.gro -p %s.top -o %s_nvt.tpr -po %s_nvt')
# os.system('%s -np 8 %s  -v -deffnm %s_nvt' % (MPIRUN, EXE))

# os.system('grompp -v -f npt.mdp -c %s_nvt.gro -p %s.top -o %s_npt.tpr -po %s_npt')
# os.system('%s -np 8 %s -v -deffnm %s_npt' % (MPIRUN, EXE))

# os.system('grompp -v -f md.mdp -c %s_npt.gro -p %s.top -o %s_md.tpr -po %s_md')

# os.chdir(testdir)


