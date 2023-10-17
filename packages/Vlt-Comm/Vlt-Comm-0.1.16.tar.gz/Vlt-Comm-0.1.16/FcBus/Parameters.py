"""
This module is used to obtain paramter characters for communication.

Current method is reading all infomation from excel which could be out of date with actual drive.
So there should be a new method reading from drive same as vltcomm in future,
 the vltcomm method is logged as below:
 1. Reading p15-92 to get all avalibe parameters' number(from 0 index to max value which reture 0);
    Then send AK = 4, IND = 6 to get the name of parameter for each one.
 2. When select one parameter, below special telegram will be sent to get characters.

    Telegram format:
    command:
    PKE(AK) = 4
    IND = 1 -- IsArray | IsEnum | DataType
          2 -- NO_OF_ARRAY_ELEMENTS
          4 -- SIZE_N_UNIT
          6 -- PARAM_NAME
          7 -- LOWER_LIMIT
          8 -- UPPER_LIMIT
          20 -- DEFAULT_VALUE
          21 -- ADDITIONAL_CHARATERISTICS

"""

class Pnu:
    def __init__(self, str_temp):
        b = str_temp.split('  ')
        c = [i for i in b if i != '']
        d = []
        for i in c:
            d.append(i.replace(' ', ''))
        self.id = int(d[0])
        self.name = d[1]
        self.items = d
        self.type = d[2]
        self.unit = d[3]
        self.scale = 10 ** (int(d[6]))
        self.enums = {}
        self.benum = False
        self.arraysize = int(d[4])
        self.all = self.all()

    def setenums(self, strlist):
        i = 0
        while i < len(strlist):
            if not int(strlist[i]) in self.enums.keys():
                self.enums[int(strlist[i])] = strlist[i + 1]
            i += 2
        self.benum = True

    def __str__(self):
        return str(self.id, self.name, self.type)

    def all(self):
        return self.id, self.name, self.type, self.unit, self.scale, self.arraysize, self.enums


class PNUs(dict):
    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        with open(filename) as file:
            ftree_tmp = self.splitfile(file)
        self.dict = {}
        self.idindex = {}
        for i in ftree_tmp:
            if i[0] != ' ':
                ptmp = Pnu(i)
                self.dict[ptmp.id] = ptmp
                self.idindex[ptmp.name] = ptmp.id
            else:
                b = i.split(' ')
                c = [i for i in b if i != '']
                self.dict[self.idindex[c[0]]].setenums(c[1:])
        self.all = sorted(list(self.keys()))

    def __getitem__(self, key):
        if isinstance(key, int):
            if key not in self.dict:
                return
            ptmp = self.dict[key]
            return ptmp
        else:
            ptmp = self.dict[self.idindex[key]]
            if key not in self.idindex:
                return
            return ptmp

    def keys(self):
        return self.dict.keys()

    @staticmethod
    def splitfile(file):
        ftree = []
        a = ''
        for i in file.readlines():
            if i != '\n':
                if i.count('//') != 0:
                    a += (i[:i.index('//')])
                else:
                    a += (i[:-1])
            else:
                ftree.append(a)
                a = ''
        return ftree

try:
    pp = PNUs(r"C:\Me\clearcase\U249250_AOC(130)_view\Holip_P618_AOC\AOC\SOURCE\Database\AutoGen\Excel.txt")
except:
    import os
    pp = PNUs(os.path.join(os.getcwd(), 'Excel.txt' ))
    print("Using local Excel.txt!")
    
    
if __name__ == '__main__':
    p = PNUs(r"C:\Me\clearcase\U249250_AOC(130)_view\Holip_P618_AOC\AOC\SOURCE\Database\AutoGen\Excel.txt")