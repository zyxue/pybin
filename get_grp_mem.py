import os
import pwd
import grp

my_gid = pwd.getpwnam(os.environ['LOGNAME']).pw_gid
users = grp.getgrgid(my_gid).gr_mem
for i in users:
    print i

