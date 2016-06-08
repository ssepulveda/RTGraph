#!/usr/bin/python3
import multiprocessing
import sys
import time
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
        self.plt1 = self.ui.plt.addPlot()
        self.img = pg.ImageItem()
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.plt1.addItem(self.img)
        self.ui.plt.addItem(self.hist)
        self.plt2 = self.ui.plt.addPlot()
        # pxMode: the spots size is independent of the zoom level
        # pen: contour
        self.scatt = pg.ScatterPlotItem(pxMode=True,
                                        pen=pg.mkPen(None))
        """
        self.plt2.setDownsampling(ds=True, auto=True, mode='peak')
        self.plt2.setClipToView(True)
        """
        self.plt2.addItem(self.scatt)

    def configure_timers(self):
        self.timer_plot_update = QtCore.QTimer(self)
        self.timer_plot_update.timeout.connect(self.update_plot)

    def configure_signals(self):
        self.ui.pButton_Start.clicked.connect(self.start)
        self.ui.pButton_Stop.clicked.connect(self.stop)
        self.ui.numIntSpinBox.valueChanged.connect(self.reset_buffers)
    
    def reset_buffers(self):
            # First argument of the fake_acq command is the number of
            # cols
            cmdargs = self.ui.cmdLineEdit.text().split(' ')
            if len(cmdargs) > 1:
                cols = int(cmdargs[1])
            else:
                cols = 512
            print("DEBUG: using {} cols".format(cols))
            self.data = RingBuffer2D(self.ui.numIntSpinBox.value(),
                                     cols=cols)
            self.time = RingBuffer2D(1, cols=cols) # Unused at the moment
            while not self.queue.empty():
                self.queue.get()
            log.info("Buffers cleared")

    def update_plot(self):
        values = []
        # Just for debugging purpose: approx. queue size
        print("Queue size: {}".format(self.queue.qsize()))
        tt = time.time()
        kk = 0
        while not self.queue.empty():
            kk+=1
            data = self.queue.get(False)
            # data is a list(time, [array,of,values])
            ts = data[0]
            values = data[1]
            #print(values)
            self.data.append(values)
            self.time.append(ts)
        #print(self.data.get_all())
        
        #print("Poped {} values".format(kk))
        if values:
            if self.ui.intCheckBox.isChecked():
                int_data = np.sum(self.data.get_all(), axis=0)
                # FIXME reshape just to make it 2D
                self.img.setImage(int_data.reshape(len(int_data),1))
                intensity = int_data[self.sensor_ids] / (2**12*self.data.rows)
                colors = [pg.intColor(200, alpha=k) for k in intensity/ np.max(intensity) * 100] 
                self.scatt.setData(x=self.x_coords,
                                   y=self.y_coords, 
                                   size=intensity,
                                   brush=colors)
            else:
                # Last value (empty queue)
                self.img.setImage(np.array(values).reshape((len(values), 1)))
                intensity = np.array(values)[self.sensor_ids] / 2**12
                colors = [pg.intColor(200, alpha=k) for k in intensity/ np.max(intensity) * 100] 
                self.scatt.setData(x=self.x_coords,
                                   y=self.y_coords, 
                                   size=intensity,
                                   brush=colors)
                
            # or integration (once the queue is empty)
            
            nt = time.time()
            print("Framerate: {} fps".format(1 / (nt - tt)))
    
    def start(self):
        log.info("Clicked start (pipe)")
        # reset buffers to ensure they have an adequate size
        self.reset_buffers()
        n_rows = 10
        n_cols = 20
        # x coords: rows. 
        self.x_coords = np.tile(np.arange(n_rows), n_cols)
        self.y_coords = np.repeat(np.arange(n_rows), n_cols)
        # corresponding sensor ids: say we use the first 300.
        self.sensor_ids = np.arange(n_rows * n_cols)
        
        # Split command and args
        cmdargs = self.ui.cmdLineEdit.text().split(' ')
        cmd = cmdargs[0]
        args = cmdargs[1:]
        self.sp = PipeProcess(self.queue,
                              cmd=cmd,
                              args=args)
        self.sp.start()
        self.timer_plot_update.start(10)


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
