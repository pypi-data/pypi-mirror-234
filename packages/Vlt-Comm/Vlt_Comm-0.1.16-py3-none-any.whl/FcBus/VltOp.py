# -------------------------------------------------------------------------------
# Name:        Vlt
# Purpose:     All base functions of vlt operation
#
# Author:      U249250
#
# Created:     20/02/2013
# Copyright:   (c) U249250 2013
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import time

import serial

from . import PnuOp
from .Support import NoDataException
from . import boot
import tqdm

class Config:
    allports = []
    product = None
    baud = 115200
    port = None
    debug = False

    def __init__(self, pt, pd):
        self.allports = pt
        self.product = pd


def gfuncs(pun):
    """
    Auto generate get/set functions for parameter get/set
    :param pun: Parmeter index
    :return: function for input paramter index
    """

    def functemp():
        return p[pun]

    if type(pun) == float:
        funcname = str(pun).replace('.', '_')
    else:
        funcname = str(pun)
    # get functions
    functemp.__name__ = 'g' + str(pun)
    globals()['g' + funcname] = functemp

    def functemp(value):
        p[pun] = value

    # set functions
    functemp.__name__ = 's' + str(pun)
    globals()['s' + funcname] = functemp
    return functemp


def gf(pun, scale = 1):
    """
    Auto generate get/set functions for parameter get/set
    :param pun: Parmeter index
    :return: function for input paramter index
    """

    def functemp():
        return p[pun] * scale

    if type(pun) == float:
        funcname = str(pun).replace('.', '_')
    else:
        funcname = str(pun)
    # get functions
    functemp.__name__ = 'g' + funcname
    return functemp


strproduct = None
cg = Config([], strproduct)
p = PnuOp.PnuOp()
Freq = 0
# p.port(cg.port)
p.baud(115200)


def gallfuncs():
    """
    Generate all parameter get and set functions,
    in form gxxx or sxxx, xxx = parameter ID

    """
    for i in range(1600, 1640):
        gfuncs(i)
    for i in range(1690, 1695):
        gfuncs(i)

    for i in range(382000, 382016):
        gfuncs(i / 100)

    for i in range(382100, 382116):
        gfuncs(i / 100)

    for i in range(386900, 386910):
        gfuncs(i / 100)


def ope():
    """
    Open the serial or if opened do nothing

    :raise ex:
    """
    try:
        if not p.s.isOpen():
            p.open()
    except Exception:
        raise


def coast():
    """
    Coast the drive

    """
    p.setCTW(0x474)


def waitfor(f, data):
    while True:
        if f() == data:
            break
        else:
            wait(0.3)


def rep0(f, times, delay=0):
    tmp = 0
    starttime = times.clock()
    while tmp < times:
        a = f()
        tmp += 1
        wait(delay)
        # if getAlarm():
        # break
        print(a)
        if a == 'OVER':
            break
    stoptime = times.clock()
    print(stoptime - starttime)


def fsw(k):
    """
    Set swith frequence
    :param k: fsw index
    :return: current fsw index
    """
    p[1401] = k
    return gfsw()


def go():
    """
    Run the drive

    """
    start()


def s():
    """
    Stop the drive

    """
    stop()


def fs():
    """
    Fast stop the drive

    """
    old = p[342]
    p[342] = 100
    s()
    p[342] = old


def gref():
    """
    Get current reference of the drive

    :return:The reference in percent
    """
    ope()
    return p.getRef()


def modbus():
    """
    Try to use modbus to switch communication setting

    """
    import minimalmodbus

    ins = minimalmodbus.Instrument(cg.port, 1)
    ins.serial.baundrate = 9600
    ins.write_register(8299, 0)
    ins.serial.close()


def detbusdelay():
    base = p.delay

    for i in range(0, 30):
        try:
            p.getRef()
        except NoDataException:
            p.setDelay(p.delay * 1.4)
        else:
            base = min(base, p.delay)
            p.setDelay(base / 2)
        print(p.delay)
    p.setDelay(base * 1.4)
    print(base * 1.4)


def findb(addr=1, port = None, newbaud=[]):
    """
    Auto detect the baud rate of Fcbus

    :raise (Exception("Can't find baud at port " + serial.device(p.s.port))):
    """
    if port is None:
        lport()

        if len(cg.allports) == 0:
            print("No 485 found at this compute!")
            try:
                cg.allports.append(int(input("Please input port number:")))
            except ValueError:
                pass

    # , 2400, 4800, 19200, 38400, 57600, 76800, 125000, 250000]
    bb = [9600, 115200]+newbaud
    bfind = False
    bcanopen = True
    bTm = False

    if p.s.isOpen():
        p.s.close()

    #Make used port high piority
    aa = [cg.port] + cg.allports if cg.port else cg.allports
    portlist = {}.fromkeys(aa).keys()

    if port is not None:
        portlist = [port]

    for i in portlist:
        print(i)
        # try boot
        try:
            print("Try boot mode...")
            b = boot.Product(i)
            if b.detectb(False):
                p.setboot(b)
                bfind = True
                bTm = True
                cg.port = i
                break
        except serial.serialutil.SerialException:
            continue
        p.setDelay(0.008)
        p.port(b.s)
        for tmp in bb:
            try:
                ope()
                p.s.baudrate = tmp
                p.setAddr(addr)
                print('try baud:', str(tmp))
                p.getRef()
            except NoDataException:
                print('Wrong baudrate!')
            except serial.serialutil.SerialException:
                p.s.close()
                print("Can't open the port at " + p.s.port)
                bcanopen = False
                break
            else:
                bfind = True
                break
        if bfind:
            try:
                if p.read(832).value != 7 and p.read(832, 8, -1).value >= 7:
                    p.write(832, 7, 0, False)
                    time.sleep(0.5)
                    p.write(832, 7, 0, False)
                    time.sleep(0.5)
                    p.s.baudrate = 115200
                p.write(835, 1, 0, False)  #set Minimum Response Delay to 1ms
                time.sleep(0.2)
                p.write(802, 1, 0, False)  #set control Source to FcBus
                time.sleep(0.2)
            except NoDataException:
                # write 832 failed so keep baundrate unchanged.
                pass
            if p.s.baudrate == 115200:
                p.setDelay(0.001)
            cg.port = i
            print("\nFound @ {} Baudrate is {}".format(p.s.port, p.read(832).value))
            # p[832]
            break
        elif bcanopen:
            print("Can't find baud at port " + p.s.port)
    return bfind, bTm


def reset(btm=False):
    """
    Cause software reset

    """
    ope()
    # noinspection PyBroadException
    try:
        p[1429] = 6111
        # p[1422] = 2
        p[1428] = 3

        if not btm:
            wait(2)
            findb()

    except Exception:
        pass


def wait(seconds):
    """
    Delay
    :param seconds: time in seconds
    """
    time.sleep(seconds)


def getpower():
    pstr = p[1541]
    try:
        power = float(pstr[pstr.index(':') + 1: -2])
    except ValueError:
        print('The power string is' + pstr)
        power = float(pstr)
    if cg.product is None:
        return True
    if power < 23:
        if cg.product != "P618":
            print("Please check product config!")
            return False

    elif power > 23:
        if cg.product != "B100":
            print("Please check product config!")
            return False
    return True


def tm():
    """
    Cause the drive into testmonitor mode

    """
    ope()
    coast()
    # if getpower():
    p.write(1429, 6111, 0, True)
    p.write(3800, 1, 0, True)
    p.write(1429, 6111, 0, True)
    p.write(3800, 1, 0, True)
    p.write(1428, 3, 0, True)
    #pclose()

def ta():
    p.ta()


def reverse():
    """
    Reverse vlt output reference
    Call twice will be back to start.

    """
    ope()
    if p.contrlWord & 0x8000:
        p.contrlWord &= 0x7fff
    else:
        p.contrlWord |= 0x8000
    p.read(101)


def start():
    """
    Let drive output

    """
    ope()
    p[801] = 2
    p[802] = 1
    p.setCTW(0x47c)


def resetctw():
    """
    Clear alarm from control words

    """
    ope()
    p.setCTW(0x4bc)
    p.setCTW(0x43c)


def gfsw():
    """

    Get Current fsw in string
    :return:string of active swith frequency
    """
    fswtable = {0: 'RAN3', 1: 'RAN5', 2: '2kHz', 3: '3kHz', 4: '4kHz', 5: '5kHz', 6: '6kHz', 7: '8kHz', 8: '10kHz',
                9: '12kHz', 10: '16kHz'}
    return fswtable[p[3821.0]]


def stop():
    """

    Stop the dirve in P342 setting
    """
    ope()
    p.setCTW(0x43c)


def ref(x):
    """
    Set the reference and start the drive
    :param x:Reference in percent
    :return:MAV
    """
    p.setCTW(0x47c)
    p.setRef(x)
    freq = x
    return str(freq) + '%', str(p[1613] / 10) + 'Hz'


def pclose():
    """

    Close the port used by this script
    """
    if p.s.isOpen:
        p.close()


def ama():
    """

    Let AMA go
    """
    s()
    p[129] = 1
    go()


def version():
    """

    Get Version of the drive
    """
    ope()
    return {"Product" : p[1543], "ACP" : p[3801.0], "MCP" : p[3801.01], "ACP_TM" : p[3801.02], "MCP_TM" : p[3801.03], "lang" : p[3801.14], "pud" : p[3801.17] }


def alarmreset():
    """
    #INTERNAL_FAUL__IOCARD_CALIBRATION_ERROR, p3887 write 85,p3886 write 10033
    #INTERNAL_FAUL__EEPROMHEADER_CKSUM_ERR, p3887 write 85,p3886 write 10001
    """
    ope()
    p[93887] = 85
    p[93886] = 10033


def eereset():
    p[93887] = 85
    p[93886] = 10001


def lport():
    """

    Auto detect serial port number occupied by RS485 from registry
    """
    import winreg

    areg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    akey = winreg.OpenKey(areg, r"Hardware\\DeviceMap\\SerialComm")

    try:
        cg.allports.clear()
        for i in range(200):
            value = winreg.EnumValue(akey, i)
            print(value)
            # if value[0].find('Silab') > 0:
            if value[1].startswith("COM"):
                port = int(value[1][3:]) - 1
                print('Find 485 port :', value[1])
                cg.allports.append(value[1])
    except EnvironmentError:
        pass
    finally:
        winreg.CloseKey(akey)


def init():
    """
    Init all parameters, will report AL80

    """
    p[1429] = 6111
    p[1422] = 2
    # reset()


def getalarm():
    """
    Get alarm word both in 1690 and 1691
    and clear the alarm word by the way
    :return:Alarmwords in 1690 and 1691
    """
    p1690 = (p[1690])
    p1691 = (p[1691])
    p1531 = p[1531]
    return p1690, p1691, p1531


def gv(num):
    return p[num]


# gallfuncs()

allvalues = {}


def gallvalues():
    '''
    Get all values of all parameters
    '''
    for i in p.pp.allpuns:
        try:
            value = p[i]
        except:
            value = None
        print(i, value)
        allvalues[i] = value


def gwait():
    return p.max_wait


def bootmode(func):
    def enclose(self, *args, **kwargs):
        if not p.detectb():
            print("Enter into testmonitor...")
            p.tm()
        return func(self, *args, **kwargs)
    return enclose


@bootmode
def laoc(filepath, toapp = True):
    '''
    load aoc bin file to the vlt
    '''
    p.laoc(None, filepath)
    if toapp:
        p.ta()


@bootmode
def llang(filepath, toapp = True):
    '''
    Load multilang bin file to the vlt
    '''
    p.llang(None, filepath)
    if toapp:
        p.ta()

@bootmode
def lmoc(filepath, toapp = True):
    '''
    load moc bin file to the vlt
    '''
    p.lmoc(None, filepath)
    if toapp:
        p.ta()


@bootmode
def lpud(filepath, toapp = True):
    '''
    Load pud file to the vlt
    '''
    p.lpud(None, filepath)
    if toapp:
        p.ta()


@bootmode
def llcp23(filepath, toapp = True):
    '''
    Load lcp23 file to the vlt
    '''
    p.llcp23(None, filepath)
    if toapp:
        p.ta()


@bootmode
def la_lang(aocfile, langfile):
    laoc(aocfile, False)
    llang(langfile, False)
    p.ta()


@bootmode
def la_lang_m(aocfile, langfile, mocfile, path=None, toapp = True):
    if path:
        import os
        os.chdir(path)
    laoc(aocfile, False)
    llang(langfile, False)
    lmoc(mocfile, False)
    if toapp:
        p.ta()

def readee(addr):
    p[3886] = addr
    return p[3887]


def readee_all(endaddr = 1024 + 1000):
    with open("ee.bin", "wb") as f:
        for i in tqdm.tqdm(range(0, endaddr)):
            dd = readee(i)
            f.write(dd.to_bytes(2,'big'))

def getA2MIF(ind):
    indd = ind + 50000
    p[3886] = indd
    return p[3887]

def getM2AIF(ind):
    indd = ind + 40000
    p[3886] = indd
    return p[3887]

def serviereset():
    p[1429] = 6111
    p[1428] = 1

def reload(pun = None):
    if pun in p.pp.paras:
        p.pp.paras.pop(pun)
    if pun is None:
        p.pp.allpuns = []
    pun = pun if pun else 101
    p[pun]
    print("Parameter counts -- {}".format(len(p.pp.allpuns)))
    if pun is None:
        return p.pp.allpuns
    else:
        return p.pp[pun].all()

def uilog(id = 0):
    return p[float((387224 + id) / 100)]