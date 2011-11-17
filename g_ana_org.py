#!/usr/bin/env python

import os
import glob
import subprocess
import Queue
from threading import Thread

__all__ = ['check_target_dirs', 'configparse', 'g_eneconv', 'g_make_ndx',
           'g_trjcat', 'g_trjconv_gro', 'g_trjconv_pro_gro', 
           'g_trjconv_pro_xtc', 'g_make_ndx']

def try_mkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    return path

def configparse(configf):
    d = {}
    with open(configf,'r') as inf:
        for line in inf:
            if line.startswith('#') or not line.strip():
                pass
            else:
                k, v = [ x.strip().strip("'") for x in line.split('=')]
                if v:
                    d[k] = v
    return d

def gen_input_files(target_dir, pf):
    input_files = dict(
        xtcf = os.path.join(target_dir, '{pf}_md.xtc'.format(pf=pf)),
        proxtcf = os.path.join(target_dir, '{pf}_pro.xtc'.format(pf=pf)),
        tprf = os.path.join(target_dir, '{pf}_md.tpr'.format(pf=pf)),
        edrf = os.path.join(target_dir, '{pf}_md.edr'.format(pf=pf)),
        grof = os.path.join(target_dir, '{pf}_md.gro'.format(pf=pf)),
        ndxf = os.path.join(target_dir, '{pf}.ndx'.format(pf=pf)))

    hb_tprf = os.path.join(target_dir, '{pf}_md_hbond.tpr'.format(pf=pf)) # potentially needed
    if os.path.isfile(hb_tprf):
        input_files.update(dict(hb_tprf=hb_tprf))
    return input_files

def runit(g_tool, kwargs_list, options, logdir):
    def worker():
        while True:
            kwargs, item = q.get()
            if options.test:
                print item
            else:
                if not options.nolog:
                    logf = '{g_tool}_{pf}.log'.format(**kwargs)
                    absolute_logf = os.path.join(logdir, logf)
                    
                    with open(absolute_logf, 'w') as opf:
                        p = subprocess.Popen(item,shell=True, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE)
                        stdoutdata, stderrdata = p.communicate()
                        opf.writelines(stdoutdata)
                        opf.writelines(stderrdata)
                        opf.write("returncode: {returncode!s}".format(returncode=p.returncode))
                else:
                    p = subprocess.call(item,shell=True)
            q.task_done()

    q = Queue.Queue()

    for i in range(16):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for kwargs in kwargs_list:
        q.put([kwargs, g_tool(kwargs)])
    
    q.join()

####################org function####################

def check_target_dirs(kwargs):
    assert os.path.exists(kwargs['target_dir'])
    s = 'echo "{target_dir} exists"'.format(**kwargs)
    return s

def g_trjcat(kwargs):
    tmpl = '{pf}_md.part[0-9][0-9][0-9][0-9].xtc'.format(**kwargs)
    xtcfs = sorted(glob.glob(os.path.join(kwargs['target_dir'], tmpl)))
    kwargs.update(dict(fmt_xtcfs=' '.join(xtcfs)))
    cmd = 'trjcat -f {fmt_xtcfs} -o {target_dir}/{pf}_md.xtc'.format(**kwargs)
    return cmd

def g_eneconv(kwargs):
    tmpl = '{pf}_md.part[0-9][0-9][0-9][0-9].edr'.format(**kwargs)
    edrfs = sorted(glob.glob(os.path.join(kwargs['target_dir'], tmpl)))
    kwargs.update(dict(fmt_edrfs=' '.join(edrfs)))
    cmd = 'eneconv -f {fmt_edrfs} -o {target_dir}/{pf}_md.edr'.format(**kwargs)
    return cmd

def g_trjconv_gro(kwargs):          # used to extract the last frame
    return 'echo "0" | trjconv -f {xtcf} -s {tprf} -pbc whole -b 199000 -dump 200000 -o {target_dir}/{pf}_md.gro'.format(**kwargs)

def g_trjconv_pro_xtc(kwargs):
    return 'echo "1" | trjconv -f {xtcf} -s {tprf} -pbc whole -o  {target_dir}/{pf}_pro.xtc'.format(**kwargs)

def g_trjconv_pro_gro(kwargs):
    return 'echo "1" | trjconv -f {xtcf} -s {tprf} -pbc whole -b 199000 -dump 200000 -o {target_dir}/{pf}_pro.gro'.format(**kwargs)

def g_make_ndx(kwargs):
    NDX_INPUTS = kwargs['ndx_inputs']
    seq = kwargs['seq']
    cdt = kwargs['cdt']
    input_  = (NDX_INPUTS['NDX_{0}'.format(cdt)] +
               NDX_INPUTS['NDX_{0}'.format(seq)])
    kwargs.update(dict(input_=input_))
    cmd = 'printf "{input_}" | make_ndx -f {grof} -o {ndxf}'.format(**kwargs)
    return cmd
