#! /usr/bin/env python

import os
import shutil
import subprocess
import StringIO
import time
from common_func import get_cpt_time, get_tpr_time
from subprocess import PIPE as pipe

class MDRun(object):
    def __init__(self, tpr, **kwargs):
        pf = tpr[:-4]
        self.pf = pf
        self.tpr = "{0}.tpr".format(pf)
        self.xtc = "{0}.xtc".format(pf)
        self.edr = "{0}.edr".format(pf)
        self.cpt = "{0}.cpt".format(pf)
        self.prev_cpt = "{0}_prev.cpt".format(pf)

        self.log = "{0}.log".format(pf)
        self.trr = "{0}.trr".format(pf)
        self.kwargs = kwargs
        if not os.path.exists(self.tpr):
            raise IOError("{0} cannot found".format(self.tpr))

    def is_first_run(self):
        if os.getenv('FIRST_RUN'):
            return True
        else:
            # Then, determine whether it's first run or not based on the
            # presences of files
            xtc_exist = os.path.exists(self.xtc)
            cpt_exist = os.path.exists(self.cpt)

            if xtc_exist and cpt_exist:
                xtc_itgy = self._check_integrity(self.xtc)
                cpt_itgy = self._check_integrity(self.cpt)     # itgy: integrity
                # check both xtc, and cpt, if corrupted, try fix it
                if not xtc_itgy:
                    if not self._fix_xtc(self.xtc, self.tpr):          # means not fixable, have to restart
                        return True
                if not cpt_itgy:
                    if not self._fix_cpt(self.cpt, self.prev_cpt):
                        return True
                return False
            elif xtc_exist and not cpt_exist:
                if self._fix_cpt(self.cpt, self.prev_cpt):
                    return False
                else:
                    return True
            else:
                return True

    def _check_integrity(self, inputfile):
        """subprocess.call return returncode"""
        r = subprocess.call(['gmxcheck', '-f', inputfile],
                            stdout=pipe, stderr=pipe)
        integrity = True if r == 0 else False
        return integrity

    def _fix_xtc(self, xtc, tpr):
        fixable = False
        p = subprocess.Popen(['trjconv', '-f', xtc, '-s', tpr, '-o', xtc],
                             stdin=pipe, stdout=pipe, stderr=pipe)
        p.communicate('0')

        bk_file = '#{0}.1#'.format(xtc)
        if os.path.exists(bk_file):
            os.remove(bk_file)

        r = subprocess.call(['gmxcheck', '-f', xtc],
                            stdout=pipe, stderr=pipe)
        if r == 0:
            fixable = True
        return fixable

    def _fix_cpt(self, cpt, prev_cpt):
        fixable = False
        if not os.path.exists(prev_cpt):
            return fixable
        else:
            r_prev_cpt = subprocess.call(['gmxcheck', '-f', prev_cpt],
                                         stdout=pipe, stderr=pipe)
            if r_prev_cpt != 0:
                return fixable
            else:
                shutil.copy(prev_cpt, cpt)
                r_cpt = subprocess.call(['gmxcheck', '-f', cpt],
                                        stdout=pipe, stderr=pipe)
                if r_cpt == 0:
                    fixable = True
                return fixable

    def _cpttime(self, cptfile):
        # different from the similar function in ~/pybin/common_func.py, this
        # one has more decimals, so is _tprtime

        stdout, stderr = subprocess.Popen(['gmxcheck', '-f', cptfile],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        # It's so stupid that gromacs-4.0.5 will direct out useful content as stderr
        for line in StringIO.StringIO(stderr):
            if 'Last frame' in line:
                sl = [i.strip() for i in line.split()]
                result = float(sl[-1])                          # unit: ps
                return result

    def _tprtime(self, tprfile):
        stdout, stderr = subprocess.Popen(['gmxdump', '-s', tprfile],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        # Different from get_cpt_time, we use stdout this time
        nsteps_found_flag = False
        dt_found_flag = False
        for line in StringIO.StringIO(stdout):
            if 'nsteps' in line:
                nsteps = float(line.split('=')[1].strip())         # number of steps
                nsteps_found_flag = True
            elif "delta_t" in line:
                dt = float(line.split('=')[1].strip())                # unit: ps
                dt_found_flag = True

            if nsteps_found_flag and dt_found_flag:
                result = float(nsteps * dt)                                   # unit: ps
                return result
                break

    def is_finished(self):
        if not os.path.exists(self.cpt):
            return False      # if cpt doesn't exist, then haven't even started the first run, yet
        cpttime = self._cpttime(self.cpt)
        tprtime = self._tprtime(self.tpr)
        if cpttime and tprtime and cpttime >= tprtime:                # cpttime, tprtime cannot be None
            return True
        else:
            return False

    def mdrun(self):
        first_run_command = ['mpirun', '-np', str(self.kwargs.get('NP', 8)), 'mdrun_mpi',
                             '-deffnm', str(self.pf), 
                             '-maxh', str(self.kwargs.get('MAXH', 24)),
                             '-cpt', str(self.kwargs.get('CPT', 15)),
                             '-npme', str(self.kwargs.get('NPME', -1))]
        if self.is_first_run():
            cmd = first_run_command
            print ' '.join(cmd)
            returncode = subprocess.call(cmd)
        else:
            cmd = first_run_command + ['-cpi', self.cpt, '-append']
            print ' '.join(cmd)
            returncode = subprocess.call(cmd)
        return returncode

