import multiprocessing
import sys
import platform
import pyqtgraph as pg
import numpy as np

import logging as log
import logging.handlers
import argparse

from pipeProcess import PipeProcess
from ringBuffer2D import RingBuffer2D
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
        self.img = pg.ImageItem()
        self.plt1.addItem(self.img)


    def configure_timers(self):
        self.timer_plot_update = QtCore.QTimer(self)
        self.timer_plot_update.timeout.connect(self.update_plot)

    def configure_signals(self):
        self.ui.pButton_Start.clicked.connect(self.start)
        self.ui.pButton_Stop.clicked.connect(self.stop)
    
    def reset_buffers(self):
            self.data = RingBuffer2D(SAMPLES)
            self.time = RingBuffer2D(1) # Unused at the moment
            while not self.queue.empty():
                self.queue.get()
            log.info("Buffers cleared")

    def update_plot(self):
        log.debug("Updating plot")
        values = []
        # Just for debugging purpose: approx. queue size
        print("Queue size: {}".format(self.queue.qsize()))
        while not self.queue.empty():
            data = self.queue.get(False)
            # data is a list(time, [array,of,values])
            ts = data[0]
            values = data[1]
            #print(values)
            self.data.append(values)
            self.time.append(ts)
        #print(self.data.get_all())
        if values:
            # Last value (empty queue)
            #self.img.setImage(np.array(values).reshape(16,32))
            # or integration (once the queue is empty)
            self.img.setImage(np.sum(self.data.get_all(), axis=0).reshape(16,32))
    
    def start(self):
        log.info("Clicked start (pipe)")
        self.sp = PipeProcess(self.queue, )
        self.sp.start()
        self.timer_plot_update.start(10)
            
    def start_serial(self):
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
