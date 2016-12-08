import multiprocessing
import logging as log

from commons.ringBuffer import RingBuffer
from processors.Serial import SerialProcess
from ui.mainWindow_ui import *

TIMEOUT = 1000
""" http://www.gnuplotting.org/tag/palette/ """
COLORS = ['#0072bd', '#d95319', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f']


class MainWindow(QtGui.QMainWindow):
    def __init__(self, port=None, bd=115200, samples=500):
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

        # configures
        self.configure_plot()
        self.configure_timers()
        self.configure_signals()

        # populate combo box for serial ports
        speeds = SerialProcess.get_serial_ports_speeds()
        self.ui.cBox_Speed.addItems(speeds)
        try:
            self.ui.cBox_Speed.setCurrentIndex(speeds.index(str(bd)))
        except:
            log.warning("Adding rare speed value to the list")
            self.ui.cBox_Speed.addItem(str(bd))
            self.ui.cBox_Speed.setCurrentIndex(len(speeds))

        if port is None:
            ports = SerialProcess.get_serial_ports()
            if len(ports) > 0:
                self.ui.cBox_Port.addItems(ports)
            else:
                log.warning("No ports found, TODO")
        else:
            log.info("Setting user specified port {}".format(port))
            self.ui.cBox_Port.addItem(port)

        self.ui.sBox_Samples.setValue(samples)


    def configure_plot(self):
        self.ui.plt.setBackground(background=None)
        self.ui.plt.setAntialiasing(True)
        self.plt1 = self.ui.plt.addPlot(row=1, col=1)

    def configure_timers(self):
        self.timer_plot_update = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer_plot_update,
                               QtCore.SIGNAL('timeout()'), self.update_plot)

    def configure_signals(self):
        self.ui.pButton_Start.clicked.connect(self.start)
        self.ui.pButton_Stop.clicked.connect(self.stop)
        self.ui.sBox_Samples.valueChanged.connect(self.update_sample_size)

    def reset_buffers(self):
        samples = self.ui.sBox_Samples.value()
        self.data = RingBuffer(samples)
        self.time = RingBuffer(samples)
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
        self.plt1.plot(x=self.time.get_all(), y=self.data.get_all(), pen=COLORS[0])

    def start(self):
        log.info("Clicked start")
        self.reset_buffers()
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

    def update_sample_size(self):
        log.info("Changing sample size")
        self.reset_buffers()


