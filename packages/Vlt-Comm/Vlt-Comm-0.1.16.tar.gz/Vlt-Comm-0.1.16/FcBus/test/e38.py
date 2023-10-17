def readee(addr):
    p[3886] = addr
    return p[3887]

def readee_all(endaddr = 1024 + 1000):
    with open("ee.bin", "wb") as f:
        for i in tqdm.tqdm(range(0, endaddr,2)):
            dd = readee(i)
            f.write(dd.to_bytes(2,'big'))

def writee(addr, val = 0):
    p[3887]=val
    p[3886]=(addr+10000)

def al38reset():
    writee(512+22)
    writee(1024+523)
    reset()

def al38test(cnts = 10):
    for i in range(0, cnts):
        print(i)
        reset()
        time.sleep(3)
        if getalarm()[0]:
            break