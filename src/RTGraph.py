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

from gui import *
from acqprocessing import AcqProcessing

class MainWindow(QtGui.QMainWindow):
    def __init__(self, acq_proc):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Know about an instance of acquisition/processing code
        # to forward GUI events
        self.acq_proc = acq_proc

        self.plt1 = None
        self.timer_plot_update = None
        self.timer_freq_update = None
        self.sp = None

        # configures
        self.configure_plot()
        self.configure_timers()
        self.configure_signals()
        
        self.sig_load_sensor_pos() # Prepare acquisition

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
        self.ui.numIntSpinBox.valueChanged.connect(self.acq_proc.reset_buffers)
        self.ui.intCheckBox.stateChanged.connect(self.sig_int_changed)
        self.ui.sensorLoadbtn.clicked.connect(self.sig_load_sensor_pos)
        self.ui.setupLoadbtn.clicked.connect(self.sig_load_setup_file)
    
    def sig_load_sensor_pos(self):
        file_path = self.ui.sensorConfFile.text()
        print("Loading sensor description file {}".format(file_path))
        data = np.genfromtxt(file_path, dtype=np.int)
        # Format is: x,y,sensor_num
        self.acq_proc.set_sensor_pos(data[:,0], data[:,1], data[:,2])
    
    def sig_int_changed(self):
        is_int = self.ui.intCheckBox.isChecked()
        self.acq_proc.set_integration_mode(is_int)
    
    def sig_load_setup_file(self):
        file_path = self.ui.setupGeneralFile.text()
        self.acq_proc.load_general_setup_file(file_path)

    def update_plot(self):
        tt = time.time()
        got_values = self.acq_proc.fetch_data()
        if not got_values: return
        data = self.acq_proc.plot_signals_map()
        intensity, colors = self.acq_proc.plot_signals_scatter()
        self.img.setImage(data.astype(np.float))
        self.scatt.setData(x=self.acq_proc.x_coords,
                            y=self.acq_proc.y_coords, 
                            size=intensity,
                            brush=colors)
        nt = time.time()
        log.info("Framerate: {} fps".format(1 / (nt - tt)))
    
    def start(self):
        log.info("Clicked start (pipe)")
        cmd = self.ui.cmdLineEdit.text()
        self.acq_proc.start_acquisition(cmd)
        self.timer_plot_update.start(10)

    def stop(self):
        log.info("Clicked stop")
        self.timer_plot_update.stop()
        self.acq_proc.stop_acquisition()


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
    
    # instance of acquisiton/processing stuff:
    ap = AcqProcessing()

    app = QtGui.QApplication(sys.argv)
    win = MainWindow(ap)
    win.show()
    app.exec()

    log.info("Finishing RTGraph\n")
    log.shutdown()
    win.close()
    app.exit()
    sys.exit()
    
