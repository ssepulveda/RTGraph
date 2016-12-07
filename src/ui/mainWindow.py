import multiprocessing
import logging as log

from commons.ringBuffer import RingBuffer
from processors.Serial import SerialProcess
from ui.mainWindow_ui import *

TIMEOUT = 1000
SAMPLES = 10


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plt1 = None
        self.timer_plot_update = None
        self.timer_freq_update = None
        self.data = None
        self.time = None
        self.sp = None

        self.queue = multiprocessing.Queue()
        self.reset_buffers()

        # configures
        self.configure_plot()
        self.configure_timers()
        self.configure_signals()

        # populate combo box for serial ports
        speeds = SerialProcess.get_serial_ports_speeds()
        ports = SerialProcess.get_serial_ports()
        self.ui.cBox_Speed.addItems(speeds)
        self.ui.cBox_Speed.setCurrentIndex(len(speeds) - 1)
        if len(ports) > 0:
            self.ui.cBox_Port.addItems(ports)
        else:
            log.warning("No ports found, TODO")

    def configure_plot(self):
        self.ui.plt.setBackground(background=None)
        self.ui.plt.setAntialiasing(True)
        self.plt1 = self.ui.plt.addPlot(row=1, col=1)

    def configure_timers(self):
        self.timer_plot_update = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer_plot_update,
                               QtCore.SIGNAL('timeout()'), self.update_plot)

    def configure_signals(self):
        QtCore.QObject.connect(self.ui.pButton_Start,
                               QtCore.SIGNAL('clicked()'), self.start)
        QtCore.QObject.connect(self.ui.pButton_Stop,
                               QtCore.SIGNAL('clicked()'), self.stop)

    def reset_buffers(self):
        self.data = RingBuffer(SAMPLES)
        self.time = RingBuffer(SAMPLES)
        while not self.queue.empty():
            self.queue.get()
        log.info("Buffers cleared")

    def update_plot(self):
        while not self.queue.empty():
            data = self.queue.get(False)
            value = data[1]
            self.data.append(value[0])
            self.time.append(data[0])

        self.plt1.clear()
        self.plt1.plot(x=self.time.get_all(), y=self.data.get_all(), pen='#2196F3')

    def start(self):
        log.info("Clicked start")
        port = self.ui.cBox_Port.currentText()
        self.sp = SerialProcess(self.queue)
        self.sp.open_port(port=port, bd=int(self.ui.cBox_Speed.currentText()))
        if self.sp.is_port_available(port):
            self.sp.start()
            self.timer_plot_update.start(10)
        else:
            log.info("Port is not available")

    def stop(self):
        log.info("Clicked stop")
        self.timer_plot_update.stop()
        if self.sp is not None:
            self.sp.stop()
            self.sp.join()
            self.reset_buffers()
