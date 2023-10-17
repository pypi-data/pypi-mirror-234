from .Support import CommandError, UnsupportPara

__author__ = 'U249250'

# from .VltOp import p
# from . import PnuOp

TYPES = {2: "E_DATATYPE_SIGNED8",
         3: "E_DATATYPE_SIGNED16",
         4: "E_DATATYPE_SIGNED32",
         5: "E_DATATYPE_UNSIGNED8",
         6: "E_DATATYPE_UNSIGNED16",
         7: "E_DATATYPE_UNSIGNED32",
         9: "E_DATATYPE_VISIBLE_STRING",
         10: "E_DATATYPE_BYTE_STRING",
         12: "E_DATATYPE_TIMEOFDAY",
         13: "E_DATATYPE_TIME_DIFFERENCE",
         20: "E_DATATYPE_SL_STRING",
         33: "E_DATATYPE_NORM_VALUE_N2",
         34: "E_DATATYPE_NORM_VALUE_N4",
         35: "E_DATATYPE_BIT_SEQUENCE",
         52: "E_DATATYPE_TIMEOFDAY_WITHOUT_DATE",
         53: "E_DATATYPE_TIME_DIFFERENCE_WITH_DATE",
         54: "E_DATATYPE_TIME_DIFFERENCE_WITHOUT_DATE",
         68: "E_DATATYPE_ERROR"
}

# def getallparas():
# for i in range(2000):
#         pno = p.read(1592, i).ret
#         if pno == 0:
#             break
#         else:
#             allpnus.append(pno)

#
# def gcharactors(pnu):
#     return p.read(pnu, 6, -1).ret

def convert(value, dtype):
    if dtype.find('_SIGNED') > 0:
        if value > 2 ** 31:
            return -2 ** 32 + value
    return value

class Pnu(object):
    def __init__(self, no, p):
        self.id = no
        chara = p.read(no, 1, -1).value
        if (chara & 0xc000) == 0xc000:
            self.isarray = True
        else:
            self.isarray = False

        if chara & 0x400:
            self.benum = True
        else:
            self.benum = False

        self.type = TYPES[chara & 0xff]

        if self.isarray:
            self.arraysize = p.read(no, 2, -1).value
        else:
            self.arraysize = 0

        temp = p.read(no, 4, -1).value
        scale = ((temp & 0xff00) >> 8)
        if scale > 128:
            scale -= 256
        self.scale = 10 ** scale
        self.unit = temp & 0xff
        self.min = convert(p.read(no, 7, -1).value, self.type) * self.scale
        self.max = convert(p.read(no, 8, -1).value, self.type) * self.scale
        self.default = convert(p.read(no, 20, -1).value, self.type)* self.scale

    def all(self):
        if self.isarray:
            return "Array", self.scale, self.benum, self.arraysize, self.default, self.id, self.isarray, self.max, self.min, self.type
        else:
            return "Not array", self.scale, self.benum, self.default, self.id, self.isarray, self.max, self.min, self.type


class Pnus(dict):
    def __init__(self, p):
        self.paras = {}
        self.p = p
        self.allpuns = []
        self.bLoad = False

    def __getitem__(self, item):
        if len(self.allpuns) == 0 or self.bLoad is False:
            print("Loading parameters:")
            self.getAllpnus()
            self.bLoad = True
        if item not in self.allpuns:
            raise UnsupportPara('The para is not supportted by this drive!')
        if item not in self.paras:
            self.paras[item] = Pnu(item, self.p)
        return self.paras[item]

    def getAllpnus(self):
        for i in range(len(self.allpuns) - 1, 2000):
            try:
                pno = self.p.read(1592, i).ret
                if pno == 0:
                    break
                else:
                    print("\r PNU:{}".format(pno), end='')
                    self.allpuns.append(pno)
            except CommandError:
                pass
        print("\n")

if __name__ == "__main__":
    findb()
    #    getallparas()
    getAllpnus()