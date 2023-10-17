"""
Created on 2011-12-1

@author: tf
"""
from struct import *
from icecream import ic

class Message(object):
    """
    classdocs
    """
    stx = 2
    lge = 14
    adr = 1
    stw = 0
    ref = 0
    cs = 0
    data = 0

    mes = 0

    def __init__(self, data, ctw=0, ref=0, addr=1):
        """
        Constructor
        """
        self.data = data
        self.stw = ctw
        if ref < 0:
            ref = 0
        self.ref = ref

    def setRef(self, ref):

        self.ref = ref

    def calBcc(self):
        self.cs = 0
        ctwa = self.stw.to_bytes(2, 'big')
        refa = self.ref.to_bytes(2, 'big')
        dataa = self.data.to_bytes(8, 'big')
        self.cs = self.stx ^ self.lge ^ self.adr
        i = 1
        while i >= 0:
            self.cs = self.cs ^ ctwa[i]
            self.cs = self.cs ^ refa[i]
            self.cs = self.cs ^ dataa[i]
            i -= 1
        self.cs = self.cs ^ dataa[2] ^ dataa[3] ^ dataa[4] ^ dataa[5] ^ dataa[6] ^ dataa[7]
        self.cs &= 0xff
        return

    def pack(self):
        # self.lge = 8 + sizeof(data)
        #self.cs = self.stx | self.lge | self.adr | self.ctw | self.ref | self.data
        self.calBcc()
        return pack('>BBBQHHB', self.stx, self.lge, self.adr, self.data, self.stw, self.ref, self.cs)



class TextMessage(Message):
    def __init__(self, data, ctw=0, ref=0, addr=1):
        super().__init__(data, ctw, ref, addr)
        self.mes = 0
        self.lge = 6 + len(self.data)

    def setMes(self, mes):
        self.mes = mes

    def calBcc(self):
        self.cs = 0
        
    def pack(self):
        self.adr |= 0x80  # STD_BUS_MY_ADDRESS
        ret = self.stx.to_bytes(1, 'big') + self.lge.to_bytes(1, 'big') + self.adr.to_bytes(1, 'big')\
            + self.data + self.stw.to_bytes(2, 'big') + self.ref.to_bytes(2, 'big')
        for i in ret:
            self.cs = self.cs ^ i
        ret += (self.cs & 0xff).to_bytes(1, 'big')
        ic(ret)
        return ret
    
    
if __name__ == '__main__':
    m = Message(0x1006000000000000, 0x474)
    ss = m.pack()
    print(ss)
    m = TextMessage('123465678')
    ss = m.pack()
    ic(ss)
