from importlib.resources import files
import time
import serial
import os
from .ymodem import Modem
from .Support import UnconfigedException, TimeOutException
import json
from .Support import singleton

resetstr = "reset"


@singleton
class Commands(object):
    def __init__(self):
        self.allcmd = json.loads(
            files('FcBus').joinpath('commands.json').read_text())

    def gcmd(self, product, cmdtype):
        assert product in ["FC360"]
        assert cmdtype in ["aoc", "lang", "moc", "pud", "lcp23"]
        return self.allcmd[product][cmdtype]


class Product(object):
    def __init__(self, port):
        if isinstance(port, int):
            portstr = "COM{}".format(port)
            s = serial.Serial(portstr)
            self.s = s
        elif isinstance(port, str):
            portstr = port
            s = serial.Serial(portstr)
            self.s = s
        else:
            self.s = port

    def serialsetting(func):
        def enclose(self, *args, **kwargs):
            # if self.s.port == None:
            #raise UnconfigedException("Config port firstly!")
            self.s.apply_settings({'baudrate': 115200, 'bytesize': 8, 'parity': 'N', 'stopbits': 1, 'xonxoff': False,
                                   'dsrdtr': False, 'rtscts': False, 'timeout': 5, 'write_timeout': 5, 'inter_byte_timeout': None})
            if not self.s.isOpen():
                self.s.open()
            return func(self, *args, **kwargs)
        return enclose

    def __run(self, cmd, filepath=None):
        print(cmd)
        if "dtm" in cmd:
            self.__write(cmd)
            self.wait_redboot(200)
        elif "load" in cmd:
            self.__write(cmd)
            self.waitCback()
            self.__ysend(filepath)
            self.wait_redboot()

    def __engine(self, cmds, filepath=None):
        for i in cmds:
            self.__run(i, filepath)

    def getback(self, cmd):
        self.__write(cmd)
        return self.wait_redboot()[2:-10].decode()

    @serialsetting
    def detectb(self, bfull = False):
        self.s.flushInput()
        self.__write("dtm timeout -t 50")
        self.wait(0.05)
        self.__write("v")
        self.wait(0.1)
        msg = self.s.read_all()
        
        if len(msg) > 0:
            if bfull:
                #set timeout back in case of long response
                print("timeout=" + self.getback("dtm timeout -t 500"))
                #FC350 /FC360
                print("type:" + self.getback("dtm moc readmem -l -a 0x0800E036"))
                #Aoc hardware version
                print("AOC hardware:" + self.getback("dtm read_version -v 18"))
                #MCP hardware version
                print("MCP hardware:" + self.getback("dtm moc readmem -s -a 0xE0042000"))
                #Power size
                print("Power size:" + self.getback("dtm moc readmem -b -d -a 0x0800E010"))
                print("Power size:" + self.getback("dtm moc readmem -b -d -a 0x0800800E"))
            return True
        else:
            return False

    def __write(self, string):
        self.s.flushInput()
        self.s.write((string + "\r").encode())

    @serialsetting
    def breset(self):
        self.__write("dtm write_ee -a 0x400 -d 0065")
        self.wait_redboot(20)
        self.__write(resetstr)

    def wait(self, tt):
        time.sleep(tt)

    @serialsetting
    def wait_redboot(self, timeout=100):
        rr = b""
        retry = 0
        while b"RedBoot>" not in rr:
            rr += self.s.read_all()
            time.sleep(0.1)
            retry += 1
            if retry > timeout:
                raise TimeOutException("TimeOut")
        return rr

    def waitCback(self, timeout=5):
        rr = b""
        retry = 0
        while b"CC" not in rr:
            rr += self.s.read_all()
            time.sleep(1)
            retry += 1
            if retry > timeout:
                raise TimeOutException("TimeOut")

    @serialsetting
    def laoc(self, startaddr, filepath):
        # self.__write("dtm flash_block_erase -s 9 -e 53")
        # self.wait_redboot()
        # self.__write("load -m yMODEM -b 0xFFE80000")
        # self.waitCback(5)
        # err = self.__ysend(filepath)
        # self.wait_redboot(5)
        # self.__write("dtm flash_block_erase -s 9 -e 9")
        # self.wait_redboot(5)
        # self.__write("dtm flash_write -a 0xFFFE7F80 -d 0123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670000E8FF00000000")
        # self.wait_redboot()
        # return err
        self.__engine(Commands().gcmd("FC360", "aoc"), filepath)

    @serialsetting
    def llang(self, startaddr, filepath):
        # for i in range(8):
        #     self.__write("dtm erase_flash -s {}".format(i))
        #     self.wait_redboot()
        # self.__write("load serialflash -m yMODEM -b 0x00")
        # self.waitCback(5)
        # self.__ysend(filepath)
        # self.wait_redboot()
        self.__engine(Commands().gcmd("FC360", "lang"), filepath)

    @serialsetting
    def lmoc(self, startaddr, filepath):
        self.__engine(Commands().gcmd("FC360", "moc"), filepath)

    @serialsetting
    def lee(self, addr, data):
        print(self.s)
        pass

    @serialsetting
    def lpud(self, addr, filepath):
        self.__engine(Commands().gcmd("FC360", "pud"), filepath)

    @serialsetting
    def llcp23(self, addr, filepath):
        self.__engine(Commands().gcmd("FC360", "lcp23"), filepath)
        
    @serialsetting
    def lall(self):
        pass

    def __ysend(self, file_path):
        self.allerror = 0

        def sender_read(size, timeout=3):
            self.s.timeout = timeout
            ret = self.s.read(size) or None
            #print("Reading %s", ret)
            return ret

        def sender_write(data, timeout=3):
            self.s.writeTimeout = timeout
            # print(data)
            return self.s.write(data)

        def callback(total_packets, success_count, error_count):
            print("\rTotal:{} success:{} error:{}".format(
                total_packets, success_count, error_count), end='')
            self.allerror += error_count

        self.s.flushInput()
        sender = Modem.Modem(sender_read, sender_write,
                             mode='ymodem1k', program="rbsb")
        file_info = {
            "name":   os.path.basename(file_path),
            "length":   os.path.getsize(file_path),
            "mtime":   os.path.getmtime(file_path),
            "source":   "win"
        }
        with open(file_path, "rb") as file_stream:
            sender.send(file_stream, retry=5,
                        callback=callback, info=file_info)
        return self.allerror

    @serialsetting
    def readmem(self, addr):
        ret = self.getback("dtm readmem -a {}".format(addr))
        return int(ret, 16)

    @serialsetting
    def readmoccal(self, cnts = 1024):
        caldata = []
        for i in range(0, cnts):
            addr = 0x800c000 + i
            cmd = "dtm moc readmem -b -d -a {}".format(addr)
            caldata.append(tsend(cmd))
        return caldata

class LoadBase(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    # b.s.close()
    logging.getLogger().setLevel(50)
    b = Product(9)
    b.laoc(0, r"C:\work\code\git\p600_aoc\ACP\Product\FC360\BuildForge\FC360.bin")

