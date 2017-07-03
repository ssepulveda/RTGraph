# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(704, 558)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Layout_controls = QtWidgets.QGridLayout()
        self.Layout_controls.setObjectName("Layout_controls")
        self.cBox_Speed = QtWidgets.QComboBox(self.centralwidget)
        self.cBox_Speed.setEditable(True)
        self.cBox_Speed.setObjectName("cBox_Speed")
        self.Layout_controls.addWidget(self.cBox_Speed, 1, 1, 1, 1)
        self.pButton_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.pButton_Stop.setObjectName("pButton_Stop")
        self.Layout_controls.addWidget(self.pButton_Stop, 1, 3, 1, 1)
        self.cBox_Port = QtWidgets.QComboBox(self.centralwidget)
        self.cBox_Port.setEditable(True)
        self.cBox_Port.setObjectName("cBox_Port")
        self.Layout_controls.addWidget(self.cBox_Port, 0, 1, 1, 1)
        self.cBox_Source = QtWidgets.QComboBox(self.centralwidget)
        self.cBox_Source.setObjectName("cBox_Source")
        self.Layout_controls.addWidget(self.cBox_Source, 0, 0, 1, 1)
        self.pButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pButton_Start.setMinimumSize(QtCore.QSize(0, 0))
        self.pButton_Start.setObjectName("pButton_Start")
        self.Layout_controls.addWidget(self.pButton_Start, 0, 3, 1, 1)
        self.sBox_Samples = QtWidgets.QSpinBox(self.centralwidget)
        self.sBox_Samples.setMinimum(1)
        self.sBox_Samples.setMaximum(100000)
        self.sBox_Samples.setProperty("value", 500)
        self.sBox_Samples.setObjectName("sBox_Samples")
        self.Layout_controls.addWidget(self.sBox_Samples, 0, 2, 1, 1)
        self.chBox_export = QtWidgets.QCheckBox(self.centralwidget)
        self.chBox_export.setEnabled(True)
        self.chBox_export.setObjectName("chBox_export")
        self.Layout_controls.addWidget(self.chBox_export, 1, 2, 1, 1)
        self.gridLayout.addLayout(self.Layout_controls, 7, 0, 1, 2)
        self.Layout_graphs = QtWidgets.QGridLayout()
        self.Layout_graphs.setObjectName("Layout_graphs")
        self.plt = GraphicsLayoutWidget(self.centralwidget)
        self.plt.setAutoFillBackground(False)
        self.plt.setStyleSheet("border: 0px;")
        self.plt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plt.setFrameShadow(QtWidgets.QFrame.Plain)
        self.plt.setLineWidth(0)
        self.plt.setObjectName("plt")
        self.Layout_graphs.addWidget(self.plt, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.Layout_graphs, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RTGraph"))
        self.pButton_Stop.setText(_translate("MainWindow", "Stop"))
        self.pButton_Start.setText(_translate("MainWindow", "Start"))
        self.sBox_Samples.setSuffix(_translate("MainWindow", " samples"))
        self.sBox_Samples.setPrefix(_translate("MainWindow", "Show "))
        self.chBox_export.setText(_translate("MainWindow", "Export to CSV"))

from pyqtgraph import GraphicsLayoutWidget
