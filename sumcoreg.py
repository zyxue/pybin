#! /usr/bin/env python

import os
import subprocess
import StringIO
from optparse import OptionParser

def main(stdoutdata, stderrdata, returncode):
    if returncode != 0 or stderrdata != '':
        raise IOError('Check the returncode: {0:d}\n and stderrdata: {1!s}\n'.format(
                returncode, stderrdata))

    accounts = os.listdir('/project/pomes')
    output = StringIO.StringIO(stdoutdata)

    ll = output.readline()
    while not ll.startswith('active jobs'):
        ll = output.readline()

    acu = {}                                                # active_cores_usage
    while not ll.startswith('eligible jobs'):
        ll, acu = collect_data(output, acu)

    ecu = {}                                              # eligible_cores_usage
    while not ll.startswith('blocked jobs'):
        ll, ecu = collect_data(output, ecu)

    bcu = {}                                               # blocked_cores_usage
    while ll:
        ll, bcu = collect_data(output, bcu)

    return acu, ecu, bcu

def run_showq():
    pipe = subprocess.PIPE
    p = subprocess.Popen('showq', stdout=pipe, stderr=pipe)
    stdoutdata, stderrdata = p.communicate()
    return stdoutdata, stderrdata, p.returncode

def collect_data(output, cores_usage):
    ll= output.readline()
    sl = ll.split()
    if len(sl) >= 9:
        user = sl[1]
        if user in accounts:
            if user in cores_usage:
                cores_usage[user] += int(sl[3])
            else:
                cores_usage[user] = int(sl[3])
    return ll, cores_usage


if __name__ == "__main__":
    accounts = os.listdir('/project/pomes')
    stdoutdata, stderrdata, returncode = run_showq()
    acu, ecu, bcu = main(stdoutdata, stderrdata, returncode)
    total_usage = {}
    for a in accounts:
        total_usage[a] = acu.get(a, 0) + ecu.get(a, 0) + bcu.get(a, 0)

    print "{0:10s} {1:8s} {2:8s} {3:8s} {4:8s}\n{5:44s}".format(
        'USERNAME', 'ACTIVE', 'ELIGIBLE', 'BLOCKED', 'TOTAL', "=" * 44)

    sorted_keys = reversed(sorted(total_usage, key=total_usage.get))
    for k in sorted_keys:
        print "{0:10s} {1:<8d} {2:<8d} {3:<8d} {4:<8d}".format(
            k, acu.get(k, 0), ecu.get(k, 0), bcu.get(k, 0), total_usage[k])
