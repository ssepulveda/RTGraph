import multiprocessing
import numpy as np
import logging as log
import pyqtgraph as pg

from ringbuffer2d import RingBuffer2D
from pipeprocess import PipeProcess

class AcqProcessing:
    def __init__(self):
        # USBBoard data format:
        # ADC data is sent in an array of size
        # size = N_uplinks_per_USB * N_channels_per_uplink
        self.num_sensors = 8*64 # for VATA64 front-end
        self.num_sensors_enabled = 8*64
        self.num_uplinks = 8
        self.num_channels_per_uplinls = 64
        self.num_integrations = 100
        
        self.integrate = False # no integration mode
        self.queue = multiprocessing.Queue()
        
        self.uplinks_enabled = None
        self.all_pedestal = 0
        self.all_pedestal_val = 0
        self.path_pedestal_file = ""
        self.all_gain = 0
        self.all_gain_val = 0
        self.path_gain_file = ""
        
        self.calibration_all_channels = dict([('pedestals',np.empty(self.num_sensors)), ('gains',np.empty(self.num_sensors))])
        
    def start_acquisition(self, cmd):
        # reset buffers to ensure they have an adequate size
        self.reset_buffers()
        self.sp = PipeProcess(self.queue,
                              cmd=cmd,
                              args=[str(self.num_sensors),])
        self.sp.start()
        
    def stop_acquisition(self):
        self.sp.stop()
        self.sp.join()
        self.reset_buffers()
    
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
    
    def fetch_data(self):
        # Just for debugging purpose: approx. queue size
        #print("Queue size: {}".format(self.queue.qsize()))
        kk = 0
        while not self.queue.empty():
            kk+=1
            raw_data = self.queue.get(False)
            self.parse_queue_item(raw_data, save=True)
            #print("Poped {} values".format(kk))
        if kk == 0: return False
        return True
    
    def plot_signals_scatter(self):
        data = self.plot_signals_map().ravel()
        intensity = data[self.sensor_ids] / (2**10*self.num_sensors)
        #colors = [pg.intColor(200, alpha=int(k)) if k!=np.NaN else 0 for k in intensity/ np.max(intensity) * 100]
        maxintensity = np.max(intensity)*0.01
        colors = [pg.intColor(200, alpha=int(k/maxintensity)) if maxintensity>0 else 0 for k in intensity] 
        return intensity, colors
    
    def plot_signals_map(self):
        if self.integrate:
            return np.sum(self.data.get_all(), axis=0).reshape(self.num_sensors,1)
        else:
            return self.data.get_partial().reshape(self.num_sensors,1)

    def set_sensor_pos(self, x_coords, y_coords, sensor_num):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.sensor_ids = sensor_num
        if np.array_equal(np.sort(sensor_num), np.arange(len(sensor_num))):
            log.warning('Sensors ID not starting at 0, or duplicated, or missing')
        
        self.reset_buffers()

    def set_num_sensors(self, value):
        self.num_sensors = value
    
    def set_integration_mode(self, value):
        self.integrate = value
    
    def reset_buffers(self):
        self.data = RingBuffer2D(self.num_integrations,
                                    cols=self.num_sensors)
        self.time = RingBuffer2D(1, cols=1) # Unused at the moment (buffer size is 1)
        self.evNumber = RingBuffer2D(1, cols=1) # Unused at the moment (buffer size is 1)            
        while not self.queue.empty():
            self.queue.get()
        log.info("Buffers cleared")
    
    def loadCSVfile(self, file_path, key):
        if not (key=='pedestals' or key=='gains'):
            log.warning("Failed to load csv file: key {} not existing!".format(key))
            return
        # load from csv file
        data = np.genfromtxt(file_path)
        # Format is: uplink, channel, data (ex pedestal, gain)
        for i,line in enumerate(data):
            # checks that the channels int the csv file are correctly ordered
            if int((line[0]%10)*self.num_channels_per_uplinls + line[1]) != i:
                log.warning("Loading {} file: Channels must be in the right order!".format(key))
            else:
                self.calibration_all_channels[key][i] = line[2]
    
    def load_general_setup_file(self, file_path):
        # load general setup file (txt)
        # which contains the uplinks enabled and where the csv ped+gain files are
        #file_path can be loaded from the interface through MainWindow class
        #file_path is passed by the MainWindow when it starts or when we want to reload it or the pedestal and gain csv files
        log.info("Loading setup file file {}".format(file_path))
        fsetup = open(file_path,'r')
        for line in fsetup:
            if not line.startswith("#"):
                para = line.replace(" ","").split('||')
                # parse the different parameters
                if para[0] == "FrontEndBoardConfig": # which uplink to enable
                    enabled = para[1:]
                    if enabled[-1]=='\n':
                        del enabled[-1]
                    if len(enabled) != 8:
                        log.warning("FrontEndBoardConfig should have 8 values and not {}! Aborting setup file loading.".format(len(enabled)))
                        return
                    self.uplinks_enabled = [int(kk) for kk in enabled]
                if para[0] == "AllPed": # applies constant pedestal to all channels
                    self.all_pedestal = int(para[1])
                if para[0] == "AllPedVal":
                    self.all_pedestal_val = int(para[1])
                if para[0] == "PathPedFile":
                    self.path_pedestal_file = para[1]
                if para[0] == "AllGain": # applies constant gain to all channels
                    self.all_gain = int(para[1])
                if para[0] == "AllGainVal":
                    self.all_gain_val = int(para[1])
                if para[0] == "PathGainFile":
                    self.path_gain_file = para[1]
        
        num_sensors = sum(x > 0 for x in self.uplinks_enabled)*self.num_channels_per_uplinls
        if num_sensors != self.num_sensors_enabled:
            self.num_sensors_enabled = num_sensors
            log.info("Number of sensors enabled changed to {}".format(num_sensors))
        
        if self.all_pedestal == 1:
            if self.all_pedestal_val > 0:
                log.info("All pedestals set to {}".format(self.all_pedestal_val))
                self.calibration_all_channels['pedestals'].fill(self.all_pedestal_val)
            else:
                log.warning("Cannot set all pedestals to ", self.all_pedestal_val, "!")
        else:
            log.info("Setting pedestals from file {}".format(self.path_pedestal_file))
            self.loadCSVfile(self.path_pedestal_file,'pedestals')
        
        if self.all_gain == 1:
            if self.all_gain_val > 0:
                log.info("All gains set to {}".format(self.all_gain_val))
                self.calibration_all_channels['gains'].fill(self.all_gain_val)
            else:
                log.warning("Cannot set all gains to ", self.all_gain_val, "!")
        else:
            log.info("Setting gains from file {}".format(self.path_gain_file))
            self.loadCSVfile(self.path_gain_file,'gains')
        
        #print(self.calibration_all_channels)
        fsetup.close()



















