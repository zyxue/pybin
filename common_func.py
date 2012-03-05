#! /usr/bin/env python

from threading import Thread
import logging
import subprocess
import Queue

def runit(cmd_logf_generator, numthread, ftest):
    """
    Putting each analyzing codes in a queue to use multiple cores simutaneously.

    The code is the same as runit in g_analyze/init2.py 2012-01-27
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

def get_cpt_time(infile, gmxcheck):
    """gmxcheck show be the absolute address of gmxcheck, so the version
    specified"""

    import StringIO

    stdout, stderr = subprocess.Popen(
        [gmxcheck,
         '-f', infile],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    # It's so stupid that gromacs-4.0.5 will direct out useful content as stderr
    for line in StringIO.StringIO(stderr):
        if 'Last frame' in line:
            sl = [i.strip() for i in line.split()]
            return_value = '{0:.0f}'.format(float(sl[-1]) / 1000)
    return return_value


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info("objects in this module is supposed to be imported rather than run directly")

