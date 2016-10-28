import multiprocessing
import logging as log

from commons.ringBuffer import RingBuffer
from processors.Serial import SerialProcess
from ui.mainWindow_ui import *

TIMEOUT = 1000
SAMPLES = 100


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
        log.debug("Updating plot")
        while not self.queue.empty():
            data = self.queue.get(False)
            value = str(data[0]).split(',')
            self.data.append(float(value[1]))
            self.time.append(data[1])

        self.plt1.clear()
        self.plt1.plot(x=self.time.get_all(), y=self.data.get_all(), pen='#2196F3')

    def start(self):
        log.info("Clicked start")
        self.sp = SerialProcess(self.queue)
        ports = self.sp.get_ports()
        log.info(ports)
        if 0 < len(ports):
            self.sp.open_port(ports[0])
            if self.sp.is_port_available(ports[0]):
                self.sp.start()
                self.timer_plot_update.start(10)
            else:
                log.info("Port is not available")
        else:
            log.warning("No ports detected")

    def stop(self):
        log.info("Clicked stop")
        self.timer_plot_update.stop()
        self.sp.stop()
        self.sp.join()
        self.reset_buffers()
