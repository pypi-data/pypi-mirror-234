import sys
import asyncio

import pyqtgraph as pg
from PySide2.QtWidgets import QApplication
from pyqtgraph.Qt import QtGui, QtCore
import time

from serial import SerialException


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        return [time.strftime("%M:%S:", time.localtime(value))+str(int((value - int(value))*1000000)) for value in values]


class ui(object):
    def __init__(self, *funcs):
        if hasattr(sys, 'frozen'):
            self.qt_app = QApplication(sys.argv)
        self.mw = pg.GraphicsLayoutWidget(show=True)
        self.label = pg.LabelItem(justify='right')
        self.mw.addItem(self.label)
        self.pw = self.mw.addPlot(row=1, col=0)
        self.pw.setAutoVisible(y=True)
        self.title = ""
        # self.mw.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.tick = 30
        # self.timer.start(self.tick)
        self.plots = {}
        self.funcs = {}
        self.names = []
        self.functypes = {}
        self.datadics = {}
        self.timedics = []
        self.args = {}
        self.bStop = False
        self.max_len = 2000
        self.pens = [(255, 0, 0), (0, 255, 0), (255, 255, 255), (0, 0, 255), (255, 255, 0), (0, 255, 255),
                     (255, 0, 255), (11, 23, 70), (3, 168, 158), (160, 32, 240)]
        self.penindex = 0
        self.pw.showGrid(True, True, 0.88)

        self.legend = pg.LegendItem((80,60), offset=(70,20))
        self.legend.setParentItem(self.pw.graphicsItem())
        self.badded = False

        if funcs:
            self.add(funcs)
        if hasattr(sys, 'frozen'):
            self.qt_app.exec_()

    def clearall(self):
        for i in self.funcs.keys():
            self.datadics[i].clear()

    def _add(self, func, functype=0, arg=()):
        # if type(func) is int or type(func) is float:
        #     func = self.func_generate(func)

        if func not in self.funcs.keys():
            self.funcs[func.__name__] = func
            self.functypes[func.__name__] = functype
            self.plots[func.__name__] = self.pw.plot(pen=self.pens[self.penindex], name = func.__name__)
            self.penindex += 1
            if self.penindex > len(self.pens):
                self.penindex = 0
            self.datadics[func.__name__] = []
            self.args[func.__name__] = arg
            self.names.append(func.__name__)
            self.legend.addItem(self.plots[func.__name__], func.__name__)

        if self.badded == False:
            p1 = self.plots[self.names[-1]]
            self.proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
            #cross hair
            self.vLine = pg.InfiniteLine(angle=90, movable=False)
            self.hLine = pg.InfiniteLine(angle=0, movable=False)
            self.pw.addItem(self.vLine, ignoreBounds=True)
            self.pw.addItem(self.hLine, ignoreBounds=True)
            self.badded = True

    def add(self, funcs):
        self.clearall()
        if isinstance(funcs, list) or isinstance(funcs, tuple):
            for i in funcs:
                self._add(i)
                self.title += (i.__name__ + '   ')
        else:
            self._add(funcs)
            self.title += funcs.__name__
        if len(self.funcs.keys()) >= 1:
            self.timer.start(self.tick * len(self.funcs.keys()))
            self.mw.setWindowTitle(self.title)
            self.mw.show()

    def remove(self, funcname):
        for i in self.funcs():
            pass

    def update(self):
        if self.mw.isHidden():
            self.stop()

        try:
            for i in self.funcs.keys():
                if self.functypes[i] == 0:
                    data = self.funcs[i]()
                elif self.functypes[i] == 1:
                    data = self.funcs[i](*self.args[i])

                if data is not None:
                    if len(self.datadics[i]) < self.max_len:
                        self.datadics[i].append(data)
                    else:
                        self.datadics[i][:-1] = self.datadics[i][1:]
                        self.datadics[i][-1] = data
                    self.timedics.append(time.time())

                newdata = self.datadics[i]
                if isinstance(newdata, list) and len(newdata) != 0:
                    self.timedics = self.timedics[-self.max_len:]
                    self.plots[i].setData(newdata)
        except SerialException:
            self.timer.stop()
            raise
        except Exception:
            pass
#        else:
#            self.stop()

    def stop(self):
        self.bStop = True
        self.timer.stop()

    def go(self):
        self.bStop = False
        self.timer.start()

    def hideEvent(self, event):
        self.stop()
        QtGui.QWidget.hide()

    def auto(self):
        self.pw.plotItem.enableAutoRange()
        self.go()

    def viewRangeChanged(self, view, range):
        print('1')
        self.sigRangeChanged.emit(self, range)
        self.pw.plotItem.enableAutoScale()

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if len(self.plots) == 0:
            return
        if self.pw.sceneBoundingRect().contains(pos):
            mousePoint = self.pw.vb.mapSceneToView(pos)
            index = int(mousePoint.x() + 0.5)
            if index >= 0 and index < len(self.datadics[self.names[0]]):
                self.labeldis(index)
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def labeldis(self, index):
        cnts = len(self.datadics)
        tstr = "<span style='font-size: 12pt'>x=%d," % (index)
        for i in range(cnts):
            tstr += "<span style='color: rgb%s'>%s=%0f</span>," % (str(self.pens[i]), self.names[i], self.datadics[self.names[i]][index])
        self.label.setText(tstr)

def plot(*args, **kargs):
    pg.plot(*args, **kargs)


if __name__ == "__main__":
    import numpy as np
    import time
    import asyncio

    async def f0():
        await asyncio.sleep(0.2)
        return np.random.normal()

    async def f1():
        await asyncio.sleep(0.2)
        return np.random.normal()*10

    def f00():
        time.sleep(0.2)
        return np.random.normal()

    def f11():
        time.sleep(0.2)
        return np.random.normal()*10

    def f2():
        return np.random.normal()*30

    u = ui(f0, f1)
    #u0 = ui(f00,f11,f2)
    u.max_len=50
    #u0.max_len = 50