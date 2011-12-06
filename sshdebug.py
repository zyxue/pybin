#! /usr/bin/env python

import subprocess
import StringIO
import logging
import re

def main():
    cmd = ['qstat']
    stdout, stderr, returncode = run_cmd(cmd)
    logging.info('{0} : {1}'.format(' '.join(cmd), returncode))
    address = parse_qstat_stdout(stdout)
    subprocess.call(['ssh', address])

def parse_qstat_stdout(stdout):
    stdoutdata = StringIO.StringIO(stdout)
    # you may be using multiple debug nodes at once, but later you will only log
    # to the first one --- zyxue: 2011-11-25.
    debugs = [ ll for ll in stdoutdata if "R debug" in ll ]
    debug_node = debugs[0].split()[0].strip()
    node_address = get_the_address(debug_node)
    return node_address

def get_the_address(debug_node):
    cmd = ['checkjob', debug_node]
    stdout, stderr, returncode = run_cmd(cmd)
    logging.info('{0} : {1}'.format(' '.join(cmd), returncode))
    stdoutdata = StringIO.StringIO(stdout)
    template = re.compile('\[gpc.*\]')
    for ll in stdoutdata:
        if template.search(ll):
            node_address = ll.strip()[1:][:-3] # when the code is written, ll is [gpc-f109n001:8]
            break
    return node_address

def run_cmd(cmd):
    """runs cmd which should be a list, and return (stdout, stderr,
    p.returncode) as a tuple"""

    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return (stdout, stderr, p.returncode)



if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    main()
