# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Dropbox\Dropbox\pw_prefs\RnD\houdini\python\pw_nodeColorize\nodeColorize.ui'
#
# Created: Sat Jun 28 23:32:42 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_nodeColorize(object):
    def setupUi(self, nodeColorize):
        nodeColorize.setObjectName("nodeColorize")
        nodeColorize.resize(309, 239)
        self.centralwidget = QtGui.QWidget(nodeColorize)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.get_btn = QtGui.QPushButton(self.centralwidget)
        self.get_btn.setObjectName("get_btn")
        self.horizontalLayout.addWidget(self.get_btn)
        self.set_btn = QtGui.QPushButton(self.centralwidget)
        self.set_btn.setObjectName("set_btn")
        self.horizontalLayout.addWidget(self.set_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.picker_ly = QtGui.QVBoxLayout()
        self.picker_ly.setObjectName("picker_ly")
        self.verticalLayout_3.addLayout(self.picker_ly)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 1)
        nodeColorize.setCentralWidget(self.centralwidget)

        self.retranslateUi(nodeColorize)
        QtCore.QMetaObject.connectSlotsByName(nodeColorize)

    def retranslateUi(self, nodeColorize):
        nodeColorize.setWindowTitle(QtGui.QApplication.translate("nodeColorize", "pw Node Colorize", None, QtGui.QApplication.UnicodeUTF8))
        self.get_btn.setText(QtGui.QApplication.translate("nodeColorize", "> GET", None, QtGui.QApplication.UnicodeUTF8))
        self.set_btn.setText(QtGui.QApplication.translate("nodeColorize", "SET >", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("nodeColorize", "Color Ramp", None, QtGui.QApplication.UnicodeUTF8))

