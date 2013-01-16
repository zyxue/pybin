import re
import os

import utils
import methods
L = utils.L

def analyze(A, C, core_vars):
    x = gen_cmds(A, C, core_vars)
    utils.runit(x, A.numthreads, A.test)

def gen_cmds(A, C, core_vars):
    for cv in core_vars:
        dpp = utils.get_dpp(cv)
        io_files = utils.gen_io_files(dpp, cv['id_'])

        kw = {}
        kw.update(cv)
        kw.update(io_files)
        kw.update(C=C)
        kw.update(vars(A)) # this is kind of dirty, parsing everything, A
                           # contains options like -b, etc

        # you can put other options derived from cv, io_files, A, C for
        # convenience for do it in the anal methods function

        root=os.path.dirname(os.path.abspath(C.filename))
        kw.update(root=root)

        kw.update(h5_filename=C['hdf5']['filename'])

        anal_func = getattr(methods, A.analysis)

        if anal_func.__module__ != methods.org.__name__:
            # methods.org.__name__: 'methods.org'
            anal_dir = os.path.join(root, C['data']['analysis'], 'r_{0}'.format(A.analysis))
            if not os.path.exists(anal_dir):
                os.mkdir(anal_dir)
            kw.update(anal_dir=anal_dir)

        L('using function: "{0}" from module "{1}"'.format(anal_func.__name__, anal_func.__module__))
        cmd = anal_func(**kw) 

        if not A.nolog:
            logd = C['data']['log']
            anal_logd = os.path.join(logd, A.analysis)
            anal_logf = os.path.join(logd, A.analysis, '{0}.log'.format(cv['id_']))
            for d in [logd, anal_logd]:
                if not os.path.exists(d):
                    os.mkdir(d)
        else:
            anal_logf = None
        yield (cmd, anal_logf)
