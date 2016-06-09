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

class AcqProcessing:
    def __init__(self):
        # USBBoard data format:
        # ADC data is sent in an array of size
        # size = N_uplinks_per_USB * N_channels_per_uplink
        self.num_sensors = 8*1 # for VATA64 front-end
        self.num_integrations = 100
        
        self.queue = multiprocessing.Queue()
    
    def parse_queue_item(self, line, save=False):
        # Here retrieve the line pushed to the queue
        # and properly parse it to return 
        # several values such as ID, time, [list of vals]
        line_items = line.split('\t')
        if len(line_items) <= 1: return None, None, None
        items = [int(kk) for kk in line_items]
        ev_num, ts, intensities = items[0], items[1], items[2:]
        if save:
            self.data.append(intensities)
            self.time.append(ts)
            self.evNumber.append(ev_num)
            
        return ev_num, ts, intensities
    
    def set_sensor_id(self, num, x_pos, y_pos):
        # Think about a good datastructure to do this.
        # Perhaps tuples (num, x_pos, y_pos) for each sensor
        # then merged to 1D arrays of x_pos, y_pos, nums
        pass
    
    def set_sensor_as_grid(rows=1, cols=1):
        """
        Assume that the values retrieved are sorted by line.
        in this case, self.n_rows = rows, self.n_cols = cols.
        If rows = 2 and cols = 3,sensor 0 is at (0, 0), while 
        sensor 1 is at (0,1), sensor 3 is at (0, 2), sensor 4 at (1,0)
        """
        if isinstance(rows, list):
            x_coords = rows # Row positions directly provided
        else:
            x_coords = np.arange(rows) # Assume unit position between each row
        if isinstance(cols, list):
            y_coords = np.arrange(cols)
        else:
            y_coords = np.arange(cols)

        # Update corresponding number of sensors
        # WARNING in we update this value$, the GUI should be updated as well.
        self.num_sensors = len(x_coords) * len(y_coords)

    def set_num_sensors(self, value):
        self.num_sensors = value
        
    def reset_buffers(self):
        self.data = RingBuffer2D(self.num_integrations,
                                    cols=self.num_sensors)
        self.time = RingBuffer2D(1,cols=1) # Unused at the moment (buffer size is 1)
        self.evNumber = RingBuffer2D(1,cols=1) # Unused at the moment (buffer size is 1)            
        while not self.queue.empty():
            self.queue.get()
        log.info("Buffers cleared")
    


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

        self.acq_proc.reset_buffers() # Prepare acquisition

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
        self.ui.numIntSpinBox.valueChanged.connect(self.acq_proc.reset_buffers)
        self.ui.numSensorSpinBox.valueChanged.connect(self.acq_proc.set_num_sensors)

    def update_plot(self):
        values = []
        # Just for debugging purpose: approx. queue size
        #print("Queue size: {}".format(self.queue.qsize()))
        tt = time.time()
        kk = 0
        queue = self.acq_proc.queue
        while not queue.empty():
            kk+=1
            raw_data = queue.get(False)
            _, _, values = self.acq_proc.parse_queue_item(raw_data, save=True)
        #print(self.acq_proc.data.get_all())
        
        #print("Poped {} values".format(kk))
        if values:
            if self.ui.intCheckBox.isChecked():
                int_data = np.sum(self.acq_proc.data.get_all(), axis=0)
                # FIXME reshape just to make it 2D
                self.img.setImage(int_data.reshape(len(int_data),1))
                intensity = int_data[self.sensor_ids] / (2**12*self.acq_proc.data.rows)
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
            #print("Framerate: {} fps".format(1 / (nt - tt)))
    
    def start(self):
        log.info("Clicked start (pipe)")
        # reset buffers to ensure they have an adequate size
        self.acq_proc.reset_buffers()
        # TODO Fix this temporary geometry
        n_rows = 2
        n_cols = self.acq_proc.num_sensors / n_rows
        # x coords: rows. 
        self.x_coords = np.tile(np.arange(n_rows), n_cols)
        self.y_coords = np.repeat(np.arange(n_rows), n_cols)
        # corresponding sensor ids: say we use the first 300.
        self.sensor_ids = range(int(n_rows * n_cols))
        
        # Split command and args
        cmd = self.ui.cmdLineEdit.text()
        self.sp = PipeProcess(self.acq_proc.queue,
                              cmd=cmd,
                              args=[str(self.acq_proc.num_sensors),])
        self.sp.start()
        self.timer_plot_update.start(10)


    def stop(self):
        log.info("Clicked stop")
        self.timer_plot_update.stop()
        self.sp.stop()
        self.sp.join()
        self.acq_proc.reset_buffers()


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
    
