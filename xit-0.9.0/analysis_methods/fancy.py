def seqspacing(**kw):
    dd = kw['C']['seqspacing']
    plk = dd['plk_fmt'].format(**kw)
    pl  = dd['pl'][plk]
    """2011-11-30: sequence_spacing.py, Andreas Vitalis, Xiaoling Wang and Rohi V.Pappu 2008 JMB"""
    # return "seqspacing.py --pf {pf} -f {proxtcf} -s {progrof} -b {b} -e {e} -l {peptide_length} -o {anadir}/{pf}_seqspacing.xvg".format(**kwargs)
    return "seqspacing.py \
-f {orderxtcf} \
-s {ordergrof} \
-b {b} \
--pl {peptide_length} \
-o {anal_dir}/{id_}_seqspacing.xvg".format(peptide_length=pl, **kw)
