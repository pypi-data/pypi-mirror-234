from .VltOp import p

class Trace(dict):
    def __init__(self):
        self.buf = {}

    # def __getitem__(self,key):
    #         return self[key]

    def logs(self, items, values):
        assert len(items) == len(values)
        i = 0
        while i < len(items):
            self.log(items[i], values[i])
            i += 1

    def log(self, itemname, value):
        if not itemname in self.keys():
            self[itemname] = []
        self[itemname].append(value)

    def get(self, itemname):
        return self[itemname]


indexid = 3872.14
dataid = 3872.13


def relog():
    p[3875.07] = 0
    p[3875.07] = 0xffff


def perflog(index):
    p[3875.07] = index
    trytime = 100
    d1 = p[indexid]
    while (d1 & 0xffffff00) != (index << 8):
        d1 = p[indexid]
        trytime -= 1
        if trytime < 0:
            return 'Error'
    dtype = d1 & 0xff
    # wait(0.2)
    data = p[dataid]
    return dtype, data


tall = []
trace = Trace()
tlist = []
tlistall = []


#@threadfunc
def getlogs():
    trace.clear()
    tlist.clear()
    a13cnts = 0
    cnts = p[3872.12]
    print('CNTS', cnts)
    b = range(0, cnts)
    perflog(0x01)
    for i in b:
        a = perflog(i)
        tlist.append(a)
        trace.log(a[0], a[1])
        print(str(a) + ',')
        if a == (100, 15):
            a13cnts += 1
        if a13cnts == 5:
            break
    tall.append(tlist)
#     import pickle
#     from time import time
#
#     fname = str(int(time()))
#     with open(fname + '_tlist.bin', 'wb') as f:
#         pickle.dump(tlist, f)
#     with open(fname + '_trace.bin', 'wb') as f:
#         pickle.dump(trace, f)

def glog(aa):
    trace.clear()
    tlist.clear()
    a13cnts = 0
    cnts = len(aa)
    print('CNTS', cnts)
    b = range(0, cnts)
    # perflog(0x01)
    for i in b:
        a = aa[i]
        tlist.append(a)
        trace.log(a[0], a[1])
        print(str(a) + ',')
        if a == (100, 15):
            a13cnts += 1
        if a13cnts == 5:
            break
    tall.append(tlist)
