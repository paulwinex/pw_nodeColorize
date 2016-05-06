from PySide.QtCore import *
from PySide.QtGui import *
import random as rn
import json
import os

historyFileName = 'pw_node_colorize_history.json'


class colorPickerClass(QWidget):
    colorChanged = Signal(QColor)
    def __init__(self, rampSize=150,
                       labelHeight=20,
                       valueRampWidhtScale=0.1,
                       gridiMargin=2,
                       gridSpasing=2,
                       showColorInfo=True,
                       useHistory=True):
        super(colorPickerClass, self).__init__()
        self.resize(100,100)
        #vars
        self.colorInfo = showColorInfo
        #ui
        self.grid = QGridLayout(self)
        self.grid.setSpacing(gridSpasing)
        self.setContentsMargins(gridiMargin,gridiMargin,gridiMargin,gridiMargin)
        #value slider
        self.value = valueSliderClass(rampSize,valueRampWidhtScale)
        #locor picker
        self.picker = colorRampClass(self, rampSize)
        self.picker.scrollSignal.connect(self.value.scrollValue)
        #color preview
        self.label = previewColorClass(self, labelHeight)
        #random button
        self.button = QPushButton('R')
        self.button.setFlat(1)
        sz = int(rampSize*valueRampWidhtScale)
        self.button.setFixedSize(QSize(sz,labelHeight))
        self.button.clicked.connect(self.randomColor)


        self.grid.addWidget(self.label,0, 1)
        self.grid.addWidget(self.picker,1, 1)
        self.grid.addWidget(self.value,1, 0)
        self.grid.addWidget(self.button,0, 0)
        if self.colorInfo:
            self.info = colorInfoClass()
            self.grid.addWidget(self.info, 2, 0, 1, 2)
            self.grid.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 0, 1, 2)
        else:
            self.grid.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 0, 1, 2)
        if useHistory:
            self.history = historyWidget(labelHeight)
            self.grid.addWidget(self.history, 0, 4, 3, 1)
        else:
            self.history = None
        #vars
        self.returnFunction = None

        #connect
        self.picker.colorChangedSignal.connect(self.colorChangedByUser)
        self.value.valueChanged.connect(self.picker.setValue)
        self.picker.valueChangedSignal.connect(self.value.setValue)
        if self.colorInfo:
            self.info.colorChanged.connect(self.colorChangedByText)
            self.blockSignals(True)
            self.updateInfo(self.getColor())
            self.blockSignals(False)
        if useHistory:
            self.history.colorFromHistorySignal.connect(self.colorFromHistory)

    def colorChangedByUser(self, color):
        self.label.setNextColor(color)
        self.colorChanged.emit(color)
        if self.colorInfo:
            self.updateInfo(color)

    def colorChangedByText(self, color):
        self.picker.blockSignals(True)
        self.label.setNextColor(color)
        self.picker.setColor(color)
        self.picker.blockSignals(False)

    def colorFromHistory(self, name):
        color = QColor(name)
        self.colorChangedByText(color)
        self.picker.setColor(color)

    def setColor(self, color):
        self.picker.setColor(color)
        # self.label.setPrevColor(color)
        if self.colorInfo:
            self.updateInfo(color)

    def getColor(self):
        return self.picker.color

    def updateInfo(self, color):
        self.info.setColorValue(color)

    def randomColor(self):
        self.setColor(QColor(rn.randrange(0,255),rn.randrange(0,255),rn.randrange(0,255)))

class colorRampClass(QWidget):
    colorChangedSignal = Signal(QColor)
    valueChangedSignal = Signal(int)
    scrollSignal = Signal(bool)
    def __init__(self, parent, size=150):
        super(colorRampClass, self).__init__()
        self.p = parent
        self.hw = size
        self.setFixedSize(QSize(self.hw, self.hw))
        self.padding = 2
        self.value = 0.0
        self.pick = [0, 0]
        self.img = None
        self.pickerSize = 8
        self.color = QColor(255,255,255)

    def paintEvent(self, event):
        if not self.img:
            self.img = self.getRamp()
        painter = QPainter()
        painter.begin(self)
        #wheel
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.drawImage(0, 0, self.img)
        #value
        painter.setPen(Qt.NoPen)
        painter.fillRect(0,0, self.hw, self.hw, QColor(0,0,0,self.value*255))
        #lines
        x = self.pick[0]
        y = self.pick[1]
        lineColor = 55 if self.value < 0.5 else 200
        painter.setPen(QPen(QColor(lineColor,lineColor,lineColor), 0.5))
        painter.drawLine(x,0,x,self.hw)
        painter.drawLine(0,y,self.hw,y)
        #picker

        painter.setPen(QPen(QColor(55,55,55), 2))
        painter.setBrush(QBrush(QColor(255,255,255)))
        painter.drawEllipse(x-self.pickerSize*0.5,
                            y-self.pickerSize*0.5,
                            self.pickerSize,
                            self.pickerSize)
        painter.end()

    def updateColor(self):
        h = self.pick[0]/float(self.hw)
        s = self.pick[1]/float(self.hw)
        v = self.value#*0.001
        c = QColor()
        c.setHsvF(h, s, 1-v)
        self.colorChangedSignal.emit(c)
        self.color = c

    def setValue(self, v):
        self.value = (1000-v) * 0.001
        self.update()
        self.updateColor()

    def mousePressEvent(self, event):
        self.setPickerPos(event.pos())
        QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.setPickerPos(event.pos())
        QWidget.mouseMoveEvent(self, event)

    def setPickerPos(self, pos):
        x = pos.x()
        y = pos.y()
        if x < 0:
            x = 0
        if x > self.hw:
            x = self.hw
        if y < 0:
            y = 0
        if y > self.hw:
            y = self.hw
        self.pick = [x, y]
        self.update()
        self.updateColor()

    def getRamp(self):
        img = QImage(self.hw, self.hw, QImage.Format_RGB32)
        color = QColor()
        for y in range(self.hw):
            for x in range(self.hw):
                h = x / float(self.hw)
                s = y/ float(self.hw)
                color.setHsvF(h, s, 1)
                img.setPixel(x, y, color.rgb())
        return img

    def setColor(self, color):
        color = QColor(color)
        color = color.toHsv()
        x = int((self.hw / 360.0 ) * color.hue())
        y = int((self.hw / 255.0 ) * color.saturation())
        v = int((1000.0 / 255) * color.value ())
        if not v == self.value:
            self.valueChangedSignal.emit(v)
        self.setPickerPos(QPoint(x,y))
        ###

    def wheelEvent(self, event):
        self.scrollSignal.emit(event.delta()<0)
        super(colorRampClass, self).wheelEvent(event)


class previewColorClass(QWidget):
    def __init__(self, parent, height=20):
        super(previewColorClass, self).__init__()
        #variables
        self.p = parent
        self.prevColor = None
        #ui
        self.ly = QHBoxLayout(self)
        self.ly.setContentsMargins(0,0,0,0)
        self.ly.setSpacing(1)
        # widgets
        self.prev = QLabel()
        self.prev.setText('')
        self.prev.setMaximumHeight(height)
        self.prev.mousePressEvent = self.restoreColor
        self.next = QLabel()
        self.next.setText('')
        self.next.setMaximumHeight(height)
        self.ly.addWidget(self.prev)
        self.ly.addWidget(self.next)
        #start
        self.prevColor = QColor(255,255,255)
        self.setPrevColor(self.prevColor)
        self.setNextColor(self.prevColor)


    def setPrevColor(self, color):
        self.prev.setStyleSheet(self.newStyle(color))
        self.prevColor = color

    def setNextColor(self, color):
        self.next.setStyleSheet(self.newStyle(color))

    def newStyle(self, color):
        if isinstance(color, QColor):
            color = color.name()
        s = '''\
QLabel{
    background-color: %s;
    border: 1px solid black;
}''' % ( color )
        return s

    def restoreColor(self, event):
        if self.prevColor:
            self.setNextColor(self.prevColor)
            self.p.picker.setColor(self.prevColor)

class valueSliderClass(QWidget):
    valueChanged = Signal(int)
    def __init__(self, size=150, width=0.2):
        super(valueSliderClass, self).__init__()
        self.height = size
        self.width = int(size*width)
        self.setFixedSize(QSize(self.width, self.height))
        self.__value = 0


        start = QPointF(0, 0)
        stop = QPointF(0, self.height)
        self.gradient = QLinearGradient(start, stop)
        self.gradient.setColorAt(0.05, QColor(255, 255, 255))
        self.gradient.setColorAt(0.95, QColor(0, 0, 0))

    def value(self):
        return self.__value

    def setValue(self, v):
        self.updateSlider(1000 - v)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        #bg
        brush = QBrush(self.gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0,0, self.width, self.height)
        #slider
        pen = QPen(QColor(250,0,0), 4)
        painter.setPen(pen)
        v = (self.height * self.__value) / 1000
        v = min(max(2,v),self.height-2)
        painter.drawLine(2, v, self.width-2,v)

        painter.end()

    def updateSlider(self, value):
        value = min(1000,max(0,value))
        if not value== self.__value:
            self.__value = value
            self.update()
            self.valueChanged.emit(1000-value)

    def mousePressEvent(self, event):
        v = event.pos().y()
        v = (v*1000)/self.height
        self.updateSlider(v)
        super(valueSliderClass, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        v = event.pos().y()
        v = (v*1000)/self.height
        self.updateSlider(v)
        super(valueSliderClass, self).mouseMoveEvent(event)
        
    def wheelEvent(self, event):

        if event.delta() < 0:
            self.scrollValue(True)
        else:
            self.scrollValue(False)

        super(valueSliderClass, self).wheelEvent(event)

    def scrollValue(self, direct):
        if direct:
            v = min(1000, self.__value + 50)
        else:
            v = max(0, self.__value - 50)
        self.updateSlider(v)


class colorInfoClass(QWidget):
    colorChanged = Signal(QColor)
    def __init__(self):
        super(colorInfoClass, self).__init__()
        self.ly = QHBoxLayout(self)
        self.ly.setContentsMargins(0,0,0,0)
        self.ly.setSpacing(2)
        self.rgbLabel = QLabel('RGB')
        self.rgbLabel.setMaximumWidth(20)
        self.rgbValue = QLineEdit()
        self.rgbValue.returnPressed.connect(self.updateByRGB)

        self.hexLabel = QLabel('HEX')
        self.hexLabel.setMaximumWidth(20)
        self.hexValue = QLineEdit()
        self.hexValue.returnPressed.connect(self.updateByHex)

        self.ly.addWidget(self.rgbLabel)
        self.ly.addWidget(self.rgbValue)
        self.ly.addWidget(self.hexLabel)
        self.ly.addWidget(self.hexValue)

    def setColorValue(self, color):
        rgb = color.red(), color.green(), color.blue()
        rgbText = ','.join([str(x) for x in rgb])
        self.rgbValue.setText(rgbText)
        hexText = color.name()
        self.hexValue.setText(hexText)

    def updateByRGB(self):
        try:
            rgb = self.rgbValue.text().strip().split(',')
            c = QColor(int(rgb[0]),int(rgb[1]),int(rgb[2]))
            self.colorChanged.emit(c)
        except:
            pass

    def updateByHex(self):
        try:
            c = QColor(self.hexValue.text())
            self.colorChanged.emit(c)
        except:
            pass

class historyWidget(QWidget):
    colorFromHistorySignal = Signal(str)
    def __init__(self, buttonHeight):
        super(historyWidget, self).__init__()
        self.main_ly = QVBoxLayout(self)
        self.main_ly.setContentsMargins(0,0,0,0)
        self.main_ly.setSpacing(0)
        self.saveHistory_btn = QPushButton()
        self.saveHistory_btn.setMaximumHeight(max(20, buttonHeight))
        self.main_ly.addWidget(self.saveHistory_btn)
        self.saveHistory_btn.setMaximumWidth(25)
        self.saveHistory_btn.setCheckable(1)
        self.saveHistory_btn.setChecked(1)
        self.saveHistory_btn.setText('')
        self.saveHistory_btn.setIconSize(QSize(16,16))
        self.saveHistory_btn.setIcon(QIcon(':/history.png'))


        self.saveHistory_btn.setContextMenuPolicy(Qt.CustomContextMenu)
        self.saveHistory_btn.customContextMenuRequested.connect(self.openMenu)


        self.scroll = QScrollArea()
        self.scroll.setMaximumWidth(28)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_ly.addWidget(self.scroll)
        self.scrollAreaWidgetContents = None
        #vars
        self.history = colorHistoryClass()
        self.updateColors()

        # conenct
        # self.saveHistory_btn.clicked.connect(self.updateColors)



    def updateColors(self):
        if self.scrollAreaWidgetContents:
            self.scrollAreaWidgetContents.setParent(None)
            del self.scrollAreaWidgetContents
        self.scrollAreaWidgetContents = QWidget()
        self.colors_ly = QVBoxLayout(self.scrollAreaWidgetContents)
        self.colors_ly.setContentsMargins(0,0,0,0)
        self.colors_ly.setSpacing(1)
        self.scroll.setWidget(self.scrollAreaWidgetContents)

        data = self.history.readData()
        self.fillColors(data['history'])

    def fillColors(self, colors):
        for color in colors:
            c = QPushButton()
            c.clicked.connect(lambda color=color:self.colorFromHistorySignal.emit(color))
            c.setFixedSize(QSize(26,26))
            c.setStyleSheet(self.frameStyle(color))
            self.colors_ly.addWidget(c)
        self.colors_ly.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def frameStyle(self, color):
        st = '''QPushButton
{
	background-color:%s;
}
''' % color
        return st

    def addColor(self, color):
        if self.saveHistory_btn.isChecked():
            self.history.addColor(color)
            self.updateColors()

    def openMenu(self):
        menu = QMenu(self)
        clearAction = QAction('Clear', self)
        @clearAction.triggered.connect
        def clearHistory():
            self.history.clear()
            self.updateColors()
        menu.addAction(clearAction)
        lenMenu = QMenu('Set History length', self)
        for i in [5,10,20,50]:
            lenMenu.addAction( QAction(str(i), self, triggered=lambda i=i:self.history.setLen(i) ) )
        menu.addMenu(lenMenu)
        menu.exec_(QCursor().pos())


class colorHistoryClass(object):
    def __init__(self):
        self.path = self.getHistoryFile()

    def getHistoryFile(self):
        home = os.getenv('APPDATA')
        if not home:
            home = os.getenv('HOME')
            if not home:
                home = os.path.expanduser('~')
        h = os.path.join(home, historyFileName)
        if not os.path.exists(h):
            self.path = h
            self.saveData(self.defaultData())
        return h

    def defaultData(self):
        return dict(history=[],
                    len=10)

    def readData(self):
        with open(self.path, 'r') as f:
            data = json.load(f)
            return data

    def saveData(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def addColor(self, name):
        # name = color.name()
        data = self.readData()
        l = data.get('len', 9)
        if not name in data['history']:
            data['history'].insert(0, name)
            data['history'] = data['history'][:l]
            self.saveData(data)

    def getColors(self):
        data = self.readData()
        return data['history']

    def setLen(self, i):
        data = self.readData()
        data['len'] = max(1,i)
        data['history'] = data['history'][:i]
        self.saveData(data)

    def clear(self):
        data = self.readData()
        data['history'] = []
        self.saveData(data)

#resources
qt_resource_data = "\x00\x00\x01\xa4\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0dIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\x09pHYs\x00\x00\x0d\xd7\x00\x00\x0d\xd7\x01B(\x9bx\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x01!IDAT8\x8d\xa5\x931\x8e\x82@\x18\x85\xbf!&\xbbW\xd8\xc4\x13l\xe3\xe2\x15V:\xca\xa9)\x08\x17\xa0 \x84j\x13\x9aY*/@8\x01%\x9dz\x05\xd1\xc6\xces\xc04\xb0\x15\x06\x011\x1b\xff\x84b\xfe\xbc\xf7\xe6{\x09#\xda\xb6\xe5\x95Y\x00\xecv\xbb#`\xfe\xd3[Z\x96\xb5^\x00h\xad;\xf3\x97m\xdb\xe79WQ\x14+\xe0\xd4]\xb8\x00\xa8\xeb\x1a\x00)\xe59\xcf\xf3=\xf0\xfd\xc0\x7f\x90Rn\xf2<\xbf\xaf\xa0\xb5\xbe-\xa4\x94\x9bg\xec}\xfd( \xcb\xb2Y\x02\xd7u7\xb3\x01\xae\xeb\xbeF\xb0\xddn\xf7B\x88I\x82\xb6m\x0f\xbe\xef?&H\x92d\x15\x86\xe1,A\x92$\xab\xfeyHp\x8a\xe3\xf8Y\x83\xbb\x19U\x00h\x9af\xad\x94*\xfb\xbb(\x8aL\xc30\x8e\xc3\x00\xa3\x0b\xe8\x7fJ\xa92\x08\x82K\x10\x04\x97N\xa8\x94*\x87\xba\x1bA]\xd7\x1ax\xeb'WU5\xc2\xed~\xb8\xa9\x0a\xbf\xc0O\xb7\xf4<\xcfL\xd3\xf4\xb3/\xf4<\xcf\x14BL\x07,\x97\xcb\xf8z\xbd~\x00\x0e\xf0\x0e\x1c\x1d\xc7\x19\x89\x07S\x02\x88W\x9f\xf3\x1f\xdc\x87\x98\x1e\xadBM\xfa\x00\x00\x00\x00IEND\xaeB`\x82"
qt_resource_name = "\x00\x0b\x06FB'\x00h\x00i\x00s\x00t\x00o\x00r\x00y\x00.\x00p\x00n\x00g"
qt_resource_struct = "\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
def qInitResources():
    qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()


if __name__ == '__main__':
    app = QApplication([])
    w = colorPickerClass(rampSize=200, showColorInfo=True)
    w.show()
    app.exec_()

