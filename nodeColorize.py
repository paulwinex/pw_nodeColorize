from PySide.QtCore import *
from PySide.QtGui import *
try:
    import hou
except:
    pass

import nodeColorize_UIs as ui
import colorPickerWidget
reload(colorPickerWidget)
import random as rn

version = 1.0

class nodeColorizeClass(QMainWindow,ui.Ui_nodeColorize):
    def __init__(self):
        super(nodeColorizeClass, self).__init__()
        self.setupUi(self)
        self.setObjectName('pw_nodeColorize_window')
        self.setWindowTitle('PW Node Colorize v%s' % version)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.picker = colorPickerWidget.colorPickerClass(200)
        self.picker_ly.addWidget(self.picker)

        self.get_btn.clicked.connect(self.getColor)
        self.set_btn.clicked.connect(self.setColor)

    def showEvent(self, event):
        super(nodeColorizeClass, self).showEvent(event)
        self.resize(10,10)
        geo = self.geometry()
        self.setFixedSize(geo.width(), geo.height())

    def setColor(self):
        color = self.picker.getColor()
        try:
            nodes = hou.selectedNodes()
            if nodes:
                c = color.getRgbF()
                for n in nodes:
                    n.setColor(hou.Color([c[0],c[1],c[2]]))
        except:
            pass
        self.picker.history.addColor(color.name())


    def getColor(self):
        try:
            nodes = hou.selectedNodes()
            if nodes:
                c = nodes[0].color().rgb()

                color = QColor.fromRgbF(c[0], c[1], c[2],1.0)
                self.picker.setColor(color)
                self.picker.label.setPrevColor(color)
        except:
            color = QColor(rn.randrange(0,255),rn.randrange(0,255),rn.randrange(0,255))
            self.picker.setColor(color)
            self.picker.label.setPrevColor(color)


if __name__ == '__main__':
    app = QApplication([])
    w = nodeColorizeClass()
    w.show()
    app.exec_()
