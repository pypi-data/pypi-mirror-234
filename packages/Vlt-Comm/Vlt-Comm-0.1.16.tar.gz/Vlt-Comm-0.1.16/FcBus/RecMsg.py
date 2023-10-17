"""
Created on 2011-12-2

@author: U249250
"""
import struct
from icecream import ic
from .Support import CommandError,ErrorDataException,NoDataException

ScaleDict = {-5: 0.00001, -4: 0.0001, -3: 0.001, -2: 0.01, -1: 0.1, 0: 1, 1: 10, 2: 100, 73: None}


class RecMsg(object):
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
    dType = 0
    pnu = 0
    index = 0
    ret = 0

    TParseDict = {3: ['name', str],
                  4: ['scale', int]}

    # 02 0E 01 1E ED 00 02 00 00 00 00 02 03 00 00 FD
    # b'\x02!\x010e\x00\x06Motor Control Principle\x04\x07\x00\x00('

    def __init__(self, data):
        """
        Constructor
        :param data:
        """
        if len(data) == 0:
            raise NoDataException('No data receieved!')

        try:
            if data[0] != 0x02:
                if 0x02 in data:
                    data = data[data.index(0x02):]
                else:
                    raise ErrorDataException('Error data receieved!')
            self.stx = data[0]
            self.lge = data[1]
            self.data = data[3: self.lge - 3]
            self.ref = int.from_bytes(data[-3:-1], 'big')
            self.value = int.from_bytes(self.data[-4:], 'big')

            self.dType = (self.data[0] >> 4)
            self.pnu = self.data[1]
            self.index = int.from_bytes(self.data[2:4], 'big')
            if self.dType == 0x3:
                if self.index == 0x6:
                    self.ret = self.data[4:self.lge - 3].decode()
                elif self.index == 0x4:
                    self.ret = ScaleDict[struct.unpack('b', self.data[6:7])[0]], int.from_bytes(self.data[7:8], 'big')
                elif self.index == 0x07 or self.index == 0x08:
                    self.ret = int.from_bytes(self.data[7:8], 'big')
                elif self.index == 0x01:
                    self.ret = int.from_bytes(self.data[7:8], 'big')

            elif self.dType == 0x02 or self.dType == 0x01:
                data = int.from_bytes(self.data[4:8], 'big')
                self.ret = data

            elif self.dType == 0x07:
                raise CommandError('Command error!')

            elif self.dType == 0x0F:
                self.ret = self.data[4:].decode()
                if self.lge > 14:
                    self.value = self.data[4:].decode()

            else:
                raise ErrorDataException('Error data receieved!')

        except IndexError:
            raise ErrorDataException('Error data receieved!')
        except UnicodeDecodeError:
            raise ErrorDataException('Error data receieved!')

    def _init__(self, recdata):
        """
        Constructor
        """
        try:
            data = struct.unpack('>BBBQHhB', recdata)
        except:
            print('recdata =', recdata)
            raise
        self.stx = data[0]
        self.lge = data[1]
        self.adr = data[2]
        self.data = data[3]
        self.stw = data[4]
        self.ref = data[5]
        self.cs = data[6]

        darray = self.data.to_bytes(8, 'big')
        self.dType = (darray[1] & 0xf0) >> 4
        self.pnu = int.from_bytes(darray[1:2], 'big')  #TODO:should be update to remove type
        self.index = int.from_bytes(darray[3:4], 'big')
        self.data = int.from_bytes(darray[5:8], 'big')

    def unPack(self):
        return self.ret


if __name__ == '__main__':
    # m = RecMsg(b'\x02!\x010e\x00\x06Motor Control Principle\x04\x07\x00\x00(')
    m = RecMsg(b'\x02\x0e\x01/\x1d\x00\x04\xff\xff\xff\xf8\x06\x03Q\xfe\x96')
    print(m.unPack())
    print(m.index)
    print(m.ret)
