import subprocess

class Mysys(object):
    def __init__(self,mysys = {
            'id' : "sq1m",
            'seq' : '(GVPGV)7',
            'cdt' : 'm',
            'tmpr' : 300,
            'scol' : 'b',
            'pcol' : 'b',
            'char' : '^', 
            'hbg' : 65,   # number of backbone hydrogen bonding groups 35*2+2-7 
            'scnpg' : 63,  # number of sidechain non-polar group, only C is considered
            'g' : 0.057143,
            'len' : 35
            }
                 ):                      
        self.id = mysys['id']
        self.seq = mysys['seq']
        self.cdt = mysys['cdt']
        self.seqcdt = self.seq + self.cdt
        self.tmpr = float(mysys['tmpr'])
        self.scol = mysys['scol']
        self.pcol = mysys['pcol']
        self.char = mysys['char']
        self.scc = mysys['scol']+mysys['char']
        self.pcc = mysys['pcol']+mysys['char']
        self.hbg = int(mysys['hbg'])
        self.scnpg = int(mysys['scnpg'])
        self.g = float(mysys['g'])
        self.len = float(mysys['len'])

def read_mysys_dat():
    mysys = {}
    import pprint
    with open('/home/zyxue/pyfiles/mysys.dat') as inf:
        l1 = inf.readline().split()                                   # keys
        for line in inf:                                              # values
            if not line.startswith('#') and line.strip():
                sys = {}
                sl = line.split()
                for k,v in zip(l1,sl):
                    if v == "None":
                        sys[k] = None
                    else:
                        sys[k] = v
                mysys[sl[0]] = Mysys(sys)
                # print mysys[sl[0]].id,
                # print mysys[sl[0]].seq,
                # print mysys[sl[0]].cdt,
                # print mysys[sl[0]].seqcdt,
                # print mysys[sl[0]].tmpr,
                # print mysys[sl[0]].pcol,
                # print mysys[sl[0]].scol,
                # print mysys[sl[0]].char,
                # print mysys[sl[0]].scc,
                # print mysys[sl[0]].pcc,
                # print mysys[sl[0]].hbg,
                # print mysys[sl[0]].scnpg,
                # print mysys[sl[0]].g,
                # print mysys[sl[0]].len
    subprocess.call('cp ~/pyfiles/mysys.dat ~/pyfiles/mysys.dat.bk',shell=True)
    return mysys

if __name__ == "__main__":
    import pprint
    pprint.pprint(read_mysys_dat())
