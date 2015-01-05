# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sat May 10 21:28:23 2014
#      by: PyQt4 UI code generator 4.10.4
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
        MainWindow.resize(625, 520)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pButton_Start = QtGui.QPushButton(self.centralwidget)
        self.pButton_Start.setMinimumSize(QtCore.QSize(0, 0))
        self.pButton_Start.setObjectName(_fromUtf8("pButton_Start"))
        self.gridLayout.addWidget(self.pButton_Start, 4, 0, 1, 1)
        self.cBox_Port = QtGui.QComboBox(self.centralwidget)
        self.cBox_Port.setObjectName(_fromUtf8("cBox_Port"))
        self.gridLayout.addWidget(self.cBox_Port, 1, 0, 1, 1)
        self.pButton_Stop = QtGui.QPushButton(self.centralwidget)
        self.pButton_Stop.setObjectName(_fromUtf8("pButton_Stop"))
        self.gridLayout.addWidget(self.pButton_Stop, 4, 1, 1, 1)
        self.cBox_Speed = QtGui.QComboBox(self.centralwidget)
        self.cBox_Speed.setObjectName(_fromUtf8("cBox_Speed"))
        self.gridLayout.addWidget(self.cBox_Speed, 1, 1, 1, 1)
        self.chBox_export = QtGui.QCheckBox(self.centralwidget)
        self.chBox_export.setObjectName(_fromUtf8("chBox_export"))
        self.gridLayout.addWidget(self.chBox_export, 5, 0, 1, 1)
        self.plt = GraphicsLayoutWidget(self.centralwidget)
        self.plt.setObjectName(_fromUtf8("plt"))
        self.gridLayout.addWidget(self.plt, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLinear_Acceleration = QtGui.QAction(MainWindow)
        self.actionLinear_Acceleration.setCheckable(True)
        self.actionLinear_Acceleration.setObjectName(_fromUtf8("actionLinear_Acceleration"))
        self.actionEuler_Rotation = QtGui.QAction(MainWindow)
        self.actionEuler_Rotation.setCheckable(True)
        self.actionEuler_Rotation.setObjectName(_fromUtf8("actionEuler_Rotation"))
        self.actionLinear_Acceleration_2 = QtGui.QAction(MainWindow)
        self.actionLinear_Acceleration_2.setCheckable(True)
        self.actionLinear_Acceleration_2.setObjectName(_fromUtf8("actionLinear_Acceleration_2"))
        self.actionG_force = QtGui.QAction(MainWindow)
        self.actionG_force.setCheckable(True)
        self.actionG_force.setChecked(True)
        self.actionG_force.setObjectName(_fromUtf8("actionG_force"))
        self.actionMeters_seg_2 = QtGui.QAction(MainWindow)
        self.actionMeters_seg_2.setCheckable(True)
        self.actionMeters_seg_2.setObjectName(_fromUtf8("actionMeters_seg_2"))
        self.actionRad_seg = QtGui.QAction(MainWindow)
        self.actionRad_seg.setCheckable(True)
        self.actionRad_seg.setChecked(True)
        self.actionRad_seg.setObjectName(_fromUtf8("actionRad_seg"))
        self.actionDeg_seg = QtGui.QAction(MainWindow)
        self.actionDeg_seg.setCheckable(True)
        self.actionDeg_seg.setObjectName(_fromUtf8("actionDeg_seg"))
        self.actionYawn_Pitch_Roll = QtGui.QAction(MainWindow)
        self.actionYawn_Pitch_Roll.setCheckable(True)
        self.actionYawn_Pitch_Roll.setChecked(True)
        self.actionYawn_Pitch_Roll.setObjectName(_fromUtf8("actionYawn_Pitch_Roll"))
        self.actionEuler_Angles = QtGui.QAction(MainWindow)
        self.actionEuler_Angles.setCheckable(True)
        self.actionEuler_Angles.setObjectName(_fromUtf8("actionEuler_Angles"))
        self.actionScan_Serial_ports = QtGui.QAction(MainWindow)
        self.actionScan_Serial_ports.setObjectName(_fromUtf8("actionScan_Serial_ports"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Serial Data Plotter", None))
        self.pButton_Start.setText(_translate("MainWindow", "Start", None))
        self.pButton_Stop.setText(_translate("MainWindow", "Stop", None))
        self.chBox_export.setText(_translate("MainWindow", "Export to CSV", None))
        self.actionLinear_Acceleration.setText(_translate("MainWindow", "Linear Acceleration", None))
        self.actionEuler_Rotation.setText(_translate("MainWindow", "Euler Rotation", None))
        self.actionLinear_Acceleration_2.setText(_translate("MainWindow", "Linear Acceleration", None))
        self.actionG_force.setText(_translate("MainWindow", "G force", None))
        self.actionMeters_seg_2.setText(_translate("MainWindow", "meters/seg^2", None))
        self.actionRad_seg.setText(_translate("MainWindow", "Rad/seg", None))
        self.actionDeg_seg.setText(_translate("MainWindow", "Deg/seg", None))
        self.actionYawn_Pitch_Roll.setText(_translate("MainWindow", "Yawn Pitch Roll", None))
        self.actionEuler_Angles.setText(_translate("MainWindow", "Euler Angles", None))
        self.actionScan_Serial_ports.setText(_translate("MainWindow", "Scan Serial ports...", None))

from pyqtgraph import GraphicsLayoutWidget
