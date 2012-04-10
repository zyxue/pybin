import ssh

for (username, hostname) in [
    ["zyxue", "login.scinet.utoronto.ca"],
    ["zhuyxue12", "colosse.clumeq.ca"],
    ["zhuyxue12", "guillimin.clumeq.ca"],
    ["zyxue", "lattice.westgrid.ca"],
    ["xuezhuyi", "pomes-mp2.ccs.usherbrooke.ca"],
    ["zyxue", "nestor.westgrid.ca"],
    ["zyxue", "orca.sharcnet.ca"],
    ["zyxue", "saw.sharcnet.ca"],
    ]:
    s = ssh.Connection(host=hostname, username=username)
    print hostname, s.execute('echo ${HOSTNAME}')
    s.close()
