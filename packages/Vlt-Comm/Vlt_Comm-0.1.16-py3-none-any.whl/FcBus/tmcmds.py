import json
import random
from importlib.resources import files
from .VltOp import p
from .tools import asciitostr

af = json.loads(files('FcBus').joinpath('tmcmds.json').read_text())

def tsend(cmdstr, timeout = 100):
    #print(cmdstr)
    p._Product__write(cmdstr)
    ret = p.wait_redboot(timeout)
    try:
        ret = ret.decode()
        #print(ret)
        ret = ret.replace('\n', '').replace('\r', '').replace('RedBoot>', '')
    except UnicodeDecodeError:
        print(ret)
    #print("=======================================================================")
    return ret

def tmaoc(af):
    for i in af["dtmaoc"]:
        cc = "dtm " + i["cmd"]
        if "go" not in cc:
            tsend(cc)

def gsn():
    a = tsend("dtm read_ee -a 0x140 -l 18")
    return asciitostr(a)


def tmmoc(af):
    for i in af["dtmmoc"]:
        cc = "dtm moc " + i["cmd"]
        if "go" in cc:
            continue
        if "normal" in cc:
            continue
        if "reset" in cc:
            continue
        if "erase" in cc:
            continue
        tsend(cc)

def tmbuildin(af):
    for i in af["buildin"]:
        cc = i["cmd"]
        if "go" not in cc:
            tsend(cc)

def ramcheck(addr = 0, val = 0x12345678):
    tsend("dtm writemem -a {} -v {}".format(addr, val))
    ret = tsend("dtm readmem -a {}".format(addr))
    assert(int(ret, 16) == val)
    ret = tsend("dtm logicmem -a {} -v 0xffffffff".format(addr))
    assert(int(ret, 16) == val)
    ret = tsend("dtm logicmem -a {} -o 0".format(addr))
    assert(int(ret, 16) == val)


def readee(addr = 0, length = 4):
    ret = tsend("dtm read_ee -a {} -l {}".format(addr, length))

def write_version(version = 2):
    tsend("dtm write_ee -a 0x364 -d {}00".format(version))

def wspecial(specil:str):
    asics = [int(ord(i)) for i in specil]
    for i in range(len(asics), 128 - 4):
        asics.append(0)

    checksum = 0
    for i in asics:
        checksum += i
    if checksum > 2**32 -1:
        checksum -= (2**32 - 1)

    asics = [hex(i)[2:] for i in asics]

    data = ''.join(asics)
    for i in range(len(data), 128 * 2 - 8):
        data += '0'

    def inttostr(dinput):
        dd = dinput.to_bytes(4,'little')
        ret = ''
        for i in dd:
            if len(hex(i)) == 4:
                ret += hex(i)[2:]
            else:
                ret += '0'
                ret += hex(i)[2:]
        return ret
    data += inttostr(checksum)
    cmd1 = "dtm write_ee -a 10240 -d {}".format(data[:128])
    cmd2 = "dtm write_ee -a 10304 -d {}".format(data[128:])
    print(cmd1)
    print(cmd2)

    ret1 = tsend(cmd1)
    ret2 = tsend(cmd2)
    return ret1, ret2


class cmds():
    def __init__(self, jsonfile):
        with open(jsonfile, encoding="utf-8") as ff:
            af = json.load(ff)


if __name__ == "__main__":
    tmaoc(af)
    tmmoc(af)
