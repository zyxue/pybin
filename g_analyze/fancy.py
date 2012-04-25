#!/env/bin/env python

import os

"""

DIFFERENCE BETWEEN fancy & basic MODULE:

analysis in fancy module is a bit more advanced than those in basic module, but
will still have output written to anadir

"""

def sequence_spacing(kwargs):
    """2011-11-30: sequence_spacing.py, Andreas Vitalis, Xiaoling Wang and Rohi V.Pappu 2008 JMB"""
    return "sequence_spacing.py --pf {pf} -f {proxtcf} -s {progrof} -b {b} -l {peptide_length} -o {anadir}/{pf}_sequence_spacing.xvg".format(**kwargs)

def conf_entropy(kwargs):
    # tmp_dir is for storing the covar_e[0-9].* directories and files in it
    # temporarily
    kwargs.update(tmp_dir=os.path.join(kwargs['anadir'], kwargs['pf']))
    # since it will be meaningless if the beginning time equals the ending time
    kwargs.update(b0 = str(int(kwargs['b'] + int(kwargs['dt']))))

    # The shit returned at this stage is really shitty!!
    return """

outputxvg={anadir}/{pf}_conf_entropy.xvg
# remove outputxvg created by previous testing run maybe
if [ -f ${{outputxvg}} ]; then rm ${{outputxvg}}; fi

for etime in {{{b0}..{e}..{dt}}}; do 
    tmp_dir={tmp_dir}
    if [ -d ${{tmp_dir}}; then rm -rf ${{tmp_dir}}; fi
    mkdir ${{tmp_dir}}

    covar_dir={tmp_dir}/covar_e${{etime}}
    if [ -d ${{covar_dir}} ]; then rm -rfv ${{covar_dir}}; fi
    mkdir ${{covar_dir}}

    printf "1\\n1\\n" | g_covar -f {proxtcf} -s {tprf} -b {b} -e ${{etime}} -mwa -o ${{covar_dir}}/eigenval_e${{etime}}.xvg -v ${{covar_dir}}/eigenvec_e${{etime}}.trr -av ${{covar_dir}}/average_e${{etime}}.pdb -l ${{covar_dir}}/covar_e${{etime}}.log
    echo ${{etime}} $(g_anaeig -v ${{covar_dir}}/eigenvec_e${{etime}}.trr -entropy 2>&1 | grep "Schlitter formula is" | awk '{{print $9}}') >> ${{outputxvg}}
done
# comment the following line when in production run
echo "returncode: 0"
   # rm -rf ${{tmp_dir}}
""".format(**kwargs)
