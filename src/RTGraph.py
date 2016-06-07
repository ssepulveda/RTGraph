import multiprocessing
import sys
import platform

import logging as log
import logging.handlers
import argparse

from serialProcess import SerialProcess
from ringBuffer import RingBuffer
from gui import *


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
        # self.timer_freq_update = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer_plot_update,
                               QtCore.SIGNAL('timeout()'), self.update_plot)
        # QtCore.QObject.connect(self.timer_freq_update,
        #                       QtCore.SIGNAL('timeout()'), self.update_freq)

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
        self.sp = SerialProcess(self.queue, simu=True)
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


def start_logging(level):
    log_format = log.Formatter('%(asctime)s,%(levelname)s,%(message)s')
    logger = log.getLogger()
    logger.setLevel(level)

    file_handler = logging.handlers.RotatingFileHandler("RTGraph.log", maxBytes=(10240 * 5), backupCount=2)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    console_handler = log.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)


def user_info():
    log.info("Platform: %s", platform.platform())
    log.info("Path: %s", sys.path[0])
    log.info("Python: %s", sys.version[0:5])


def man():
    parser = argparse.ArgumentParser(description='RTGraph\nA real time plotting and logging application')
    parser.add_argument("-l", "--log",
                        dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level")
    return parser


if __name__ == '__main__':
    multiprocessing.freeze_support()
    args = man().parse_args()
    if args.logLevel:
        start_logging(args.logLevel)
    else:
        start_logging(log.INFO)
    user_info()

    log.info("Starting RTGraph")

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()

    log.info("Finishing RTGraph\n")
    log.shutdown()
    win.close()
    app.exit()
    sys.exit()
