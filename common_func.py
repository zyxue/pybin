#! /usr/bin/env python

import os
from threading import Thread
import logging
import subprocess
import shutil
import Queue
import StringIO

def runit(cmd_logf_generator, numthread, ftest):
    """
    Putting each analyzing codes in a queue to use multiple cores simutaneously.

    The code is the same as runit in g_analyze/init2.py 2012-01-27

    Just learned this is called load-balancing! 2012-09-25
    """
    def worker():
        while True:
            cmd, logf = q.get()
            if ftest:
                print cmd
            else:
                logging.info('working on {0:s}'.format(cmd))
                if logf is None:
                    p = subprocess.call(cmd, shell=True)
                else:
                    with open(logf, 'w') as opf:
                        p = subprocess.Popen(cmd, shell=True, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE)
                        for data in p.communicate():
                            opf.writelines(data)          # both stdout & stderr
                        opf.write(
                            "{0:s} # returncode: {1:d}\n".format(
                                cmd, p.returncode))
            q.task_done()

    q = Queue.Queue()

    for i in range(numthread):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for cmd_logf in cmd_logf_generator:
        q.put(cmd_logf)
    
    q.join()

def get_cpt_time(infile):
    proc = subprocess.Popen(['gmxcheck', '-f', infile],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        # It's strange that gromacs-4.[05].5 will direct out useful content as stderr
        for line in StringIO.StringIO(stderr):
            if 'Last frame' in line:
                sl = [i.strip() for i in line.split()]
                return_value = '{0:.0f}'.format(float(sl[-1]) / 1000)     # unit: ns
                return return_value
    else:
        if not os.path.exists(infile):
            return "{0} not exist".format(infile)
        else:
            return "{0} is corrupted".format(infile)

def get_tpr_time(tprfile):
    proc = subprocess.Popen(['gmxdump', '-s', tprfile],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if proc.returncode == 0:
        # Different from get_cpt_time, we use stdout this time
        nsteps_found_flag = False
        dt_found_flag = False
        for line in StringIO.StringIO(stdout):
            if 'nsteps' in line:
                nsteps = float(line.split('=')[1].strip())  # number of steps
                nsteps_found_flag = True
            elif "delta_t" in line:
                dt = float(line.split('=')[1].strip())      # unit: ps
                dt_found_flag = True

            if nsteps_found_flag and dt_found_flag:
                break
        result = "{0:.0f}".format(nsteps * dt / 1000)       # unit: ns
        return result
    else:
        if not os.path.exists(tprfile):
            return "{0} not exist".format(tprfile)
        else:
            return "{0} is corrupted".format(tprfile)

def backup_file(f):
    if os.path.exists(f):
        dirname = os.path.dirname(f)
        basename = os.path.basename(f)
        count = 1
        rn_to = os.path.join(
            dirname, '#' + basename + '.{0}#'.format(count))
        while os.path.exists(rn_to):
            count += 1
            rn_to = os.path.join(
                dirname, '#' + basename + '.{0}#'.format(count))
        print "BACKING UP {0} to {1}".format(f, rn_to)
        shutil.copy(f, rn_to)
        return rn_to
        print "BACKUP FINISHED"

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info("objects in this module is supposed to be imported rather than run directly")

