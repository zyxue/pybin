#! /usr/bin/env python

import time
import subprocess
from optparse import OptionParser

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""
PROBALEM TO SOLVE:
This script probably only works on linux(Ubuntu) the whole directory will be
monitored instead of a single file, don't know how to do that, so however the
directory is modified, the python file specified will be re-executed
"""

class ModifyingEventHandler(FileSystemEventHandler):
    """re-execute the path file after modification"""
    def on_modified(self, event):
        super(ModifyingEventHandler, self).on_modified(event)
        subprocess.call(['clear'])                          # clear screen of previous output
        if options.pyfile:
            subprocess.call(['python', options.pyfile])
        elif options.cmd:
            subprocess.call(options.cmd, shell=True)

def parse_cmd():
    parser = OptionParser('usage: %prog [options] **args')
    parser.add_option('-p', type='str', dest='path', default='.', 
                      help='the directory you want to monitor')
    parser.add_option('-f', type='str', dest='pyfile', default=None, 
                      help='the python file you want to re-execute everytime it is changed')
    parser.add_option('-c', type='str', dest='cmd', default=None, 
                      help='the cmd you want to re-execute everytime it is changed')

    options, args = parser.parse_args()
    return options

if __name__ == "__main__":
    options = parse_cmd()

    handler = ModifyingEventHandler()
    o = Observer()
    o.schedule(handler, path=options.path, recursive=False)
    o.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        o.stop()
    o.join()
