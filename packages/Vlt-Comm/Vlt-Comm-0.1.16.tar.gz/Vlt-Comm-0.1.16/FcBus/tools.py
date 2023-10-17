import time

def rep(fcode, cnts = 1, tsleep = 1):
    for i in range(0, cnts):
        print(i)
        fcode()

        time.sleep(tsleep)


def asciitostr(asstr):
    def cut(ss, cnt = 1):
        return [ss[i:i+cnt] for i in range(0, len(ss), cnt)]

    aa  = cut(asstr, 2)
    ret = ""
    for i in aa:
        ret += chr(int(i, 16))
    return ret