#!/usr/bin/env python
import sys
from gui import *
from serialProcess import SerialProcess
from multiprocessing import Queue
from collections import deque
from csvExport import CSVExport
from serialPorts import getSerialPorts
from log import Log

##
# @brief Buffer size for the data (number of points in the plot)
WINDOW = 1024
##
# @brief Update time of the plot, in ms
PLOT_UPDATE_TIME = 10
##
# @brief Point to update in each redraw
PUS = -100


##
# @briefManaging and plotting acquired data
# @param QtGui.QMainWindow Qt4 Main Window reference
class MainWindow(QtGui.QMainWindow):
    ##
    # @brief Configures initial settings of the window.
    # Initialize data, plots, imported functions and timers
    # @param self Object handler
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        try:
            QtGui.QApplication.setGraphicsSystem('opengl')
            self.ui.plt.setAntialiasing(True)
        except:
            log.i('Failed to use OpenGL for plotting')
            raise
            pass

        # Initializes plots
        self.plt1 = self.ui.plt.addPlot(row=1, col=1)

        # Variables
        self.reset_buffers()
        self.queue = Queue(WINDOW)
        self.data = None
        self.csv = None
        self.DATA0 = []
        self.TIME = []

        ##
        # @brief Reference update plot timer
        # Qt4 timer to trigger the @updatePlot function
        self.timer = QtCore.QTimer(self)

        # Qt signals and slots
        QtCore.QObject.connect(self.ui.pButton_Start,
                               QtCore.SIGNAL('clicked()'), self.start)
        QtCore.QObject.connect(self.ui.pButton_Stop,
                               QtCore.SIGNAL('clicked()'), self.stop)
        QtCore.QObject.connect(self.timer,
                               QtCore.SIGNAL('timeout()'), self.update_plot)

        # Configure UI
        ports = getSerialPorts()
        if len(ports) <= 0:
            ans = QtGui.QMessageBox.question(self,
                                             "No serial ports avaliable",
                                             "Connect a serial device.\n" +
                                             "Scan again?",
                                             QtGui.QMessageBox.Yes,
                                             QtGui.QMessageBox.No)
            if ans == QtGui.QMessageBox.Yes:
                ports = getSerialPorts()
        self.ui.cBox_Port.addItems(ports)
        self.ui.cBox_Speed.addItems(["9600", "57600", "115200"])
        self.ui.cBox_Speed.setCurrentIndex(0)
        self.set_ui_locked(False)

        # Configure plots
        # self.configurePlot(self.ui.plt1, "Euler Angles", "degree", [-180, 180])

    ##
    # @brief Start SerialProcess for data acquisition
    # @param self Object handler
    def start(self):
        self.data = SerialProcess(self.queue)
        # Select serial port configuration form ui
        self.data.openPort(str(self.ui.cBox_Port.currentText()),
                           int(self.ui.cBox_Speed.currentText()))

        if self.data.start() is False:
            QtGui.QMessageBox.question(self,
                                       "Can't open Serial Port",
                                       "Serial port is already opened.",
                                       QtGui.QMessageBox.Ok)
        else:
            # start CSV data export if enabled
            if self.ui.chBox_export.isChecked():
                # export data
                self.csv = CSVExport()
                self.ui.statusbar.showMessage("Exporting data")
            else:
                self.ui.statusbar.showMessage("Acquiring data")
            # start data process, lock the ui and set plot update time
            self.set_ui_locked(True)
            self.timer.start(PLOT_UPDATE_TIME)

    ##
    # @brief Updates buffer values, removing old ones
    # @param self Object handler
    # @param buffer_ Buffer to be updated
    # @param data New data to be appended
    def update_buffer(self, buffer_, data):
        buffer_.append(data)
        if len(buffer_) > WINDOW:
            buffer_.pop(0)

    ##
    # @brief Updates graphs and writes to CSV files if enabled
    # @param self Object handler
    def update_plot(self):
        # Get new data from buffer
        while self.queue.qsize() != 0:
            data = self.queue.get(True, 1)
            self.update_buffer(self.TIME, data[0])
            self.update_buffer(self.DATA0, data[1])
            # If enabled, write to log file
            if self.ui.chBox_export.isChecked():
                self.csv.csvWrite(data)
        # Draw new data
        self.plt1.clear()
        self.plt1.plot(x=self.TIME[-PUS:], y=self.DATA0[-PUS:], pen='r')

    ##
    # @brief Stops SerialProcess for data acquisition
    # @param self Object handler
    def stop(self):
        self.data.closePort()
        self.data.join()
        self.timer.stop()
        self.set_ui_locked(False)
        self.reset_buffers()
        self.ui.statusbar.showMessage("Stopped data adquisition")

    ##
    # @brief Basic configurations for a plot
    # @param self Object handler
    # @param plot Plot to be customized
    # @param title Title for the plot
    # @param unit Unit for the plot
    # @param plot_range List with min and max values to show in the plot
    def configure_plot(self, plot, title, unit, plot_range=[0, 0]):
        plot.setLabel('left', title, unit)
        plot.setLabel('bottom', 'Time', 's')
        # plot.showGrid(x=True, y=True)
        plot.showGrid(x=False, y=True)
        if plot_range[0] != 0 and plot_range[1] != 0:
            plot.setYRange(plot_range[0], plot_range[1])
        plot.setMouseEnabled(x=False, y=False)

    ##
    # @brief Basic configurations for a plot
    # @param self Object handler
    # @param enabled Sets the ui locked
    def set_ui_locked(self, enabled):
        self.ui.pButton_Stop.setEnabled(enabled)
        self.ui.pButton_Start.setEnabled(not enabled)
        self.ui.cBox_Port.setEnabled(not enabled)
        self.ui.cBox_Speed.setEnabled(not enabled)
        self.ui.chBox_export.setEnabled(not enabled)

    ##
    # @brief Clears the buffers
    # @param self Object handler
    def reset_buffers(self):
        self.DATA0 = []
        self.TIME = []

    ##
    # @brief Function to be executed while closing the main window
    # @param self Object handler
    # @param event Event who calls the exit
    def closeEvent(self, event):
        log.i('Starting close')
        try:
            if self.data.is_alive():
                log.w('SerialProcess running, stopping it')
                self.stop()
        except:
            pass
        app.exit()
        sys.exit()

if __name__ == "__main__":
    # configuring log
    log = Log('main')
    if '-v' in sys.argv:
        log.level('INFO')
    elif '-vv' in sys.argv:
        log.level('DEBUG')
    else:
        log.level('ERROR')

    log.i('Starting Application')
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    app.exec_()
