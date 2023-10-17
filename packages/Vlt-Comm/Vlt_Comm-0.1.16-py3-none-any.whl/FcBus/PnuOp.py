"""
Created on 2011-12-4

@author: tf
"""
import math
import threading
import time
import serial
from . import ParaOp, boot
from .RecMsg import RecMsg
from .SndMsg import *
from .Support import CommandError, UnsupportPara, ErrorDataException, NoDataException

ParaType = {3869: 'S32',
            3821: 'S32',
            3820: 'U32'}


def getpnu(k):
    if isinstance(k, int):
        index = 0
        pint = k
    else:
        pint = math.trunc(k)
        index = int((k - pint) * 100 + 0.5)
    return pint, index


def grecdata(sinput):
    try:
        ret = RecMsg(sinput)
        return True, ret
    except ErrorDataException:
        return False, None


class PnuOp(tuple, boot.Product):
    """
    classdocs
    This class is used for Vlt control.

    """
    data = [1, 2, 3, 4, 5, 6]
    index = 0
    # {9600: 0.1, 115200: 0.015, 2400: 0.35, 4800: 0.25, 19200: 0.01, 38400: 0.01, 57600: 0.01, 76800: 0.01,
    delay = 0.015
    # 250000: 0.01, 125000: 0.01}
    contrlWord = 0
    ref = 0
    refw = 0
    lock = threading.Lock()
    debug = False
    log = []
    cntlog = []
    ret = None

    def __init__(self, product=None, addr = 1):
        """
        Constructor
        """
        self.s = serial.Serial()
        self.s.parity = 'E'
        # self.s.setTimeout(3)
        self.s.baundrate = 115200
        self.pp = ParaOp.Pnus(self)
        self.addr = addr

    def serialsetting(func):
        def enclose(self, *args, **kwargs):
            if self.s.port == None:
                raise UnconfigedException("Config port firstly!")
            self.s.apply_settings({'baudrate': 115200, 'bytesize': 8, 'parity': 'E', 'stopbits': 1, 'xonxoff': False,
                                   'dsrdtr': False, 'rtscts': False, 'timeout': 5, 'write_timeout': 5, 'inter_byte_timeout': None})
            if not self.s.isOpen():
                self.s.open()
            return func(self, *args, **kwargs)
        return enclose

    def __setitem__(self, k, v):
        """
        Use "PnuOp[pnu] = data" to set parameter's value
        """
        try:
            pnu, index = getpnu(k)
            if type(v) is not str:
                v /= self.pp[pnu].scale
                v = int(v)
            ret = self.write(pnu, v, index, True)

            if self.debug:
                print(pnu, v, index)
            import inspect
            if 'module' in inspect.currentframe().f_back.f_code.co_name:
                print(ret.value.strip("\x00"))
        except AttributeError:
            return None

    def __getitem__(self, k):
        """
        Use "PnuOp[pnu]" to get the value of parameter
        """
        return self._readpnu0(k)

    def _readpnu(self, k):
        return self.read(k).value

    def _readpnu0(self, k):
        try:
            pnu, index = getpnu(k)
            if self.pp[pnu].arraysize != 0:
                if type(k) == int:
                    ret = []
                    for i in range(self.pp[pnu].arraysize):
                        if self.pp[pnu].type == 'E_DATATYPE_VISIBLE_STRING':
                            ret.append(self.read(pnu, i, "Text").ret)
                        else:
                            try:
                                val = self.convert(pnu,self.read(pnu, i).ret) * self.pp[pnu].scale
                            except CommandError:
                                val = None
                            ret.append(val)
                    return ret

            if self.pp[pnu].type == 'E_DATATYPE_VISIBLE_STRING':
                d = self.read(pnu, index, "Text")
                v = d.ret if d is not None else None
                return v
            else:
                v = self.convert(pnu, self.read(pnu, index).ret)

            # Since not supported by Holip, removed
            if self.pp[pnu].benum:
                try:
                    return v, self.pp[pnu].enums[v]
                except KeyError:
                    raise
                except AttributeError:
                    pass

            return v * self.pp[pnu].scale

        except UnsupportPara:
            print("Unsupported parameter!")

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]

    max_wait = 0

    def _read_try(self, data, index=0, rtype=0):
        '''
        Add two input para index and rtype to decide whether use fix length telegram or not.
        '''
        delay = self.delay
        cnts = 0
        bfixmode = True
        waitcnts = []

        if index == 20 or rtype == "Text":
            bfixmode = False
        try:
            self.lock.acquire()
            self.s.flushInput()
            self.s.write(data)
            if bfixmode:
                while (self.s.inWaiting() < 14):
                    # cnt = self.s.inWaiting()
                    #if cnt > 0:
                       # print(cnt)
                    if self.debug:
                        print(self.s.inWaiting())
                    time.sleep(delay)
                    cnts += 1
                    if cnts > 20:
                        raise NoDataException('Time out!')
            else:
                while cnts < 50:
                    cnts += 1
                    time.sleep(delay)
                    waitcnts.append(self.s.inWaiting())
                    if waitcnts.count(max(waitcnts)) > 5 and max(waitcnts) > 6:
                        break
                    elif cnts > 40:
                        raise NoDataException('Time out!')
            self.max_wait = cnts
            stemp = self.s.read(self.s.inWaiting())
            cnts = 0
            rr = grecdata(stemp)
            while rr[0] == False:
                rr = grecdata(stemp + self.s.read(self.s.inWaiting()))
                time.sleep(delay)
                cnts += 1
                if cnts > 20:
                    raise NoDataException('Time out!')

        # except ErrorDataException:
            # ret = None
        finally:
            self.lock.release()
        return rr[1]

    def read(self, pnu, index=0, rtype=0):
        """The low level function for reading data from drive"""
        if self.debug:
            print("Read -- ", pnu, index, rtype)
        snd = SndMsg(rtype, pnu, index)
        snd.setCtw(self.contrlWord)
        snd.setRef(self.refw)
        snd.setAddr(self.addr)
        snd = snd.pack()

        cnts = 0
        while(cnts < 50):
            cnts += 1
            self.ret = self._read_try(snd, index, rtype)
            if self.ret is not None:
                break
            else:
                self.log.append((index, self.ret))
        return self.ret

    def baud(self, baud):
        self.s.baudrate = baud

    def port(self, port):
        if isinstance(port, str):
            self.s.setPort(port)
        elif isinstance(port, serial.Serial):
            self.s = port
        self.s.parity = "E"
        self.s.stopbits = 1
        self.s.bytesize = 8

    def open(self):
        self.s.open()

    def close(self):
        self.s.close()

    def write(self, pnu, data, index=0, bread=True):
        try:
            if type(data) is str:
                typet = "Text"
            else:
                if pnu > 90000:  # if pun is larger than 90000,it should be EEPROM opration
                    typet = 3
                    pnu -= 90000
                else:
                    typet = 3
                if data < 0x10000:
                    pass
                else:
                    typet = typet + 1

            snd = SndMsg(typet, pnu, index, data)

            snd.setAddr(self.addr)
            snd.setCtw(self.contrlWord)
            snd.setRef(self.refw)

            if not bread:
                try:
                    self.lock.acquire()
                    self.s.write(snd.pack())
                finally:
                    self.lock.release()
            else:
                self.ret = self._read_try(snd.pack())

        except CommandError:
            print("ERROR!! -- Please make sure the command is right!")
        return self.ret

    def setDelay(self, ms):
        self.delay = ms

    def setCTW(self, controlword):
        self.contrlWord = controlword | (self.contrlWord & 0x8000)
        self.read(1592)

    def setRef(self, reference):
        reference *= (0x4000 / 100)
        self.refw = int(reference)
        self.read(1592)

    def getRef(self):
        """Get referenc from driver"""
        return self.read(1592).ref / (0x4000 / 100)

    def getSRef(self):
        """Get static reference,don't read from drive"""
        return self.ret.ref / (0x4000 / 100)

    def getSStw(self):
        """Get static status,don't read from drive"""
        if self.ret is None:
            return 0
        return self.ret.stw

    def getSTW(self):
        """Get status from driver"""
        return hex(self.read(1592).stw)

    def getScale(self, no):
        """Get the scale for one parameter"""

    def getName(self, pnu):
        b = SndMsg(5, pnu, 6, 0).pack()
        print(b)
        self.s.write(b)
        time.sleep(self.delay)
        stemp = self.s.read(self.s.inWaiting())
        print(stemp)
        self.ret = RecMsg(stemp).unPack()
        return self.ret

    def convert(self, no, value):
        no = int(no)
        if no in ParaType.keys():
            if ParaType[no] == 'S32':
                if value > 2 ** 31:
                    return -2 ** 32 + value
        elif self.pp[no].type.find('_SIGNED') > 0:
            if value > 2 ** 31:
                return -2 ** 32 + value
        return value

    def setboot(self, boot: boot.Product):
        self._b = boot
        self.s = boot.s

    def ta(self):
        self.breset()
        # self.port(self._b.s)
        self.s.apply_settings({'baudrate': 115200, 'bytesize': 8, 'parity': 'E', 'stopbits': 1, 'xonxoff': False,
                               'dsrdtr': False, 'rtscts': False, 'timeout': 5, 'write_timeout': 5, 'inter_byte_timeout': None})

    @serialsetting
    def tm(self):
        self.write(1429, 6111)
        self.write(3800, 1)
        self.write(1429, 6111)
        self.write(1428, 3)
        self.wait_redboot()
        # self._b = boot.Product(self.s)

    def adetect(self, newbaud):
        bfind = False
        self.s.baudrate = newbaud
        try:
            self.s.open()
            self.getRef()
        except NoDataException:
            print('Wrong baudrate!')
        except serial.serialutil.SerialException:
            p.s.close()
            print("Can't open the port at " + p.s.port)
            bcanopen = False
        else:
            bfind = True
            print('Found!')
        return bfind

    def setAddr(self, addr):
        self.addr = addr

"""     def __getattribute__ (self, name):
        print(name)
        if name in ["laoc", "llang"]:
            return object.__getattribute__(self._b, name)
        else:
            return object.__getattribute__(self, name)  """

