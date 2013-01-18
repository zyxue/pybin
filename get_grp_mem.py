import os
import pwd
import grp

"""this script tries to generate a list of members in my group"""

my_gid = pwd.getpwnam(os.environ['LOGNAME']).pw_gid
users = grp.getgrgid(my_gid).gr_mem
if users:
    users = [user for user in users]
else:                       # on some clusters, this could be []. e.g. orca
    users = [user.pw_name for user in pwd.getpwall() if user.pw_gid == my_gid]

for i in users:
    print i
