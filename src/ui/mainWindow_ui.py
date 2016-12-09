# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(704, 558)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet(_fromUtf8(""))
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Layout_controls2 = QtGui.QGridLayout()
        self.Layout_controls2.setObjectName(_fromUtf8("Layout_controls2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.Layout_controls2.addItem(spacerItem, 0, 1, 1, 1)
        self.chBox_export = QtGui.QCheckBox(self.centralwidget)
        self.chBox_export.setEnabled(False)
        self.chBox_export.setObjectName(_fromUtf8("chBox_export"))
        self.Layout_controls2.addWidget(self.chBox_export, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Layout_controls2, 9, 1, 1, 1)
        self.Layout_controls = QtGui.QGridLayout()
        self.Layout_controls.setObjectName(_fromUtf8("Layout_controls"))
        self.cBox_Speed = QtGui.QComboBox(self.centralwidget)
        self.cBox_Speed.setObjectName(_fromUtf8("cBox_Speed"))
        self.Layout_controls.addWidget(self.cBox_Speed, 0, 1, 1, 1)
        self.cBox_Port = QtGui.QComboBox(self.centralwidget)
        self.cBox_Port.setEditable(False)
        self.cBox_Port.setObjectName(_fromUtf8("cBox_Port"))
        self.Layout_controls.addWidget(self.cBox_Port, 0, 0, 1, 1)
        self.pButton_Start = QtGui.QPushButton(self.centralwidget)
        self.pButton_Start.setMinimumSize(QtCore.QSize(0, 0))
        self.pButton_Start.setObjectName(_fromUtf8("pButton_Start"))
        self.Layout_controls.addWidget(self.pButton_Start, 2, 0, 1, 1)
        self.pButton_Stop = QtGui.QPushButton(self.centralwidget)
        self.pButton_Stop.setObjectName(_fromUtf8("pButton_Stop"))
        self.Layout_controls.addWidget(self.pButton_Stop, 2, 1, 1, 1)
        self.sBox_Samples = QtGui.QSpinBox(self.centralwidget)
        self.sBox_Samples.setMinimum(1)
        self.sBox_Samples.setMaximum(100000)
        self.sBox_Samples.setProperty("value", 500)
        self.sBox_Samples.setObjectName(_fromUtf8("sBox_Samples"))
        self.Layout_controls.addWidget(self.sBox_Samples, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.Layout_controls, 7, 0, 1, 2)
        self.Layout_graphs = QtGui.QGridLayout()
        self.Layout_graphs.setObjectName(_fromUtf8("Layout_graphs"))
        self.plt = GraphicsLayoutWidget(self.centralwidget)
        self.plt.setAutoFillBackground(False)
        self.plt.setStyleSheet(_fromUtf8("border: 0px;"))
        self.plt.setFrameShape(QtGui.QFrame.StyledPanel)
        self.plt.setFrameShadow(QtGui.QFrame.Plain)
        self.plt.setLineWidth(0)
        self.plt.setObjectName(_fromUtf8("plt"))
        self.Layout_graphs.addWidget(self.plt, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Layout_graphs, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "RTGraph", None))
        self.chBox_export.setText(_translate("MainWindow", "Export to CSV", None))
        self.pButton_Start.setText(_translate("MainWindow", "Start", None))
        self.pButton_Stop.setText(_translate("MainWindow", "Stop", None))
        self.sBox_Samples.setSuffix(_translate("MainWindow", " samples", None))
        self.sBox_Samples.setPrefix(_translate("MainWindow", "Show ", None))

from pyqtgraph import GraphicsLayoutWidget
