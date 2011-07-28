import sys
import os
import glob
import stat

"""used to change the first line of python script to "#!/usr/bin/env python\n"""

infs = glob.glob('*.py')
for inf in infs:
    if inf != sys.argv[0] and not os.path.isdir(inf) :
        os.rename(inf, "%s.bk" % inf)

infs = glob.glob('*.bk')

for inf in infs:
    if inf != sys.argv[0] and not os.path.isdir(inf) :
        newf = inf.replace('.bk', '')
        oldf = open(inf, 'r')
        newf = open(newf, 'w')
        newf.write('#!/usr/bin/env python\n')
        for line in oldf:
            if line.startswith('#!'):
                pass 
            else:
                newf.write(line)
        newf.close()
        oldf.close()
        os.chmod(newf.name, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    else:
        pass
