import os
import subprocess
import StringIO

def g_select(**kw):
    CG = kw['C']['g_select']
    ndx_fn = CG['repo_ndx_tmpl'].format(**kw)
    kw['repo_ndx'] = os.path.join(kw['root'], kw['C']['data']['repository'], ndx_fn)
    gssk = CG['g_sel_sel_key_tmpl'].format(**kw)
    kw['g_sel_sel'] = CG[gssk]
    return """g_select \
-f {grof} \
-s {tprf} \
-on {repo_ndx} \
-select '{g_sel_sel}'""".format(**kw)

def symlink_ndx(**kw):
    CG = kw['C']['g_select']
    ndx_fn = CG['repo_ndx_tmpl'].format(**kw)
    kw['repo_ndx'] = os.path.join(kw['root'], kw['C']['data']['repository'], ndx_fn)

    return "ln -s -f -v {repo_ndx} {ndxf}".format(**kw)

def extend_tpr(**kw):
    T = kw['tprf']
    tm = get_tpr_time(T)
    nr = os.path.basename(T).rsplit('.tpr')[0]              # nr: name root
    renamed = '{0}_{1}ns.tpr'.format(nr, tm)
    kw.update(oldtprf=os.path.join(os.path.dirname(T), renamed))
    return 'mv -v {tprf} {oldtprf}; tpbconv -s {oldtprf} -extend {extend} -o {tprf}'.format(**kw)

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
