import multiprocessing
import numpy as np
import logging as log
import pyqtgraph as pg
import yaml
import itertools

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
        self.num_channels_per_uplinks = 64
        self.num_integrations = 100
        
        self.integrate = False # no integration mode
        self.queue = multiprocessing.Queue()
        
        self.uplinks_enabled = None
        self.channels_enabled = None
        self.all_pedestal = 0
        self.all_pedestal_val = 0
        self.path_pedestal_file = ""
        self.all_gain = 0
        self.all_gain_val = 0
        self.path_gain_file = ""
        
        self.calibration_all_channels = dict([('pedestals',np.empty(self.num_sensors_enabled)), ('gains',np.empty(self.num_sensors_enabled))])
        
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
            # all ADC values from USBboard are in intensities
            # takes ADC values selected (channels enabled) with the setup file
            intensities = list(itertools.compress(intensities, self.channels_enabled)) # ceci prend ~5us
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
        intensity = data[self.sensor_ids] / (2**10*self.num_sensors_enabled)
        #colors = [pg.intColor(200, alpha=int(k)) if k!=np.NaN else 0 for k in intensity/ np.max(intensity) * 100]
        maxintensity = np.max(intensity)*0.01
        colors = [pg.intColor(200, alpha=int(k/maxintensity)) if maxintensity>0 else 0 for k in intensity] 
        return intensity, colors
    
    def plot_signals_map(self):
        if self.integrate:
            return np.sum(self.data.get_all(), axis=0).reshape(self.num_sensors_enabled,1)
        else:
            return self.data.get_partial().reshape(self.num_sensors_enabled,1)

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
                                    cols=self.num_sensors_enabled)
        self.time = RingBuffer2D(1, cols=1) # Unused at the moment (buffer size is 1)
        self.evNumber = RingBuffer2D(1, cols=1) # Unused at the moment (buffer size is 1)            
        while not self.queue.empty():
            self.queue.get()
        log.info("Buffers cleared")
    
    def loadCSVfile(self, file_path, key):
        if not (key == 'pedestals' or key == 'gains'):
            log.warning("Failed to load csv file: key {} not existing!".format(key))
            return
        # load from csv file
        data = np.genfromtxt(file_path)
        all_calib = np.empty(self.num_sensors)
        # Format is: uplink, channel, data (ex pedestal, gain)
        for i, line in enumerate(data):
            # checks that the channels int the csv file are correctly ordered
            if int((line[0] % 10) * self.num_channels_per_uplinks + line[1]) != i:
                log.warning("Loading {} file: Channels must be in the right order!".format(key))
            else:
                all_calib[i] = line[2]
        self.calibration_all_channels[key] = list(itertools.compress(all_calib, self.channels_enabled))
    
    def load_general_setup_file(self, file_path):
        # load general setup file (txt)
        # which contains the uplinks enabled and where the csv ped+gain files are
        #file_path can be loaded from the interface through MainWindow class
        #file_path is passed by the MainWindow when it starts or when we want to reload it or the pedestal and gain csv files
        log.info("Loading setup file {}".format(file_path))
        
        with open(file_path, 'r') as f:
            cfg = yaml.load(f)
        
        if len(cfg['FrontEndBoardConfig']) != 8:
            og.warning("FrontEndBoardConfig should have 8 values and not {}! Aborting setup file loading.".format(len(enabled)))
            return
        
        self.uplinks_enabled = cfg['FrontEndBoardConfig']
        self.all_pedestal = cfg['Pedestals']['AllPed']
        self.all_pedestal_val = cfg['Pedestals']['AllPedVal']
        self.path_pedestal_file =  cfg['Pedestals']['PedFilePath']
        
        self.all_gain = cfg['Gains']['AllGain']
        self.all_gain_val = cfg['Gains']['AllGainVal']
        self.path_gain_file =  cfg['Gains']['GainFilePath']
        
        # updates channels enabled:
        self.channels_enabled = [enabled for enabled in self.uplinks_enabled for _ in range(self.num_channels_per_uplinks)]
        
        num_sensors = sum(x > 0 for x in self.uplinks_enabled) * self.num_channels_per_uplinks
        if num_sensors != self.num_sensors_enabled:
            self.num_sensors_enabled = num_sensors
            log.info("Number of sensors enabled changed to {}".format(num_sensors))
            self.reset_buffers()
        
        if self.all_pedestal:
            if self.all_pedestal_val > 0:
                log.info("All pedestals set to {}".format(self.all_pedestal_val))
                self.calibration_all_channels['pedestals'].fill(self.all_pedestal_val)
            else:
                log.warning("Cannot set all pedestals to ", self.all_pedestal_val, "!")
        else:
            log.info("Setting pedestals from file {}".format(self.path_pedestal_file))
            self.loadCSVfile(self.path_pedestal_file, 'pedestals')
        
        if self.all_gain:
            if self.all_gain_val > 0:
                log.info("All gains set to {}".format(self.all_gain_val))
                self.calibration_all_channels['gains'].fill(self.all_gain_val)
            else:
                log.warning("Cannot set all gains to ", self.all_gain_val, "!")
        else:
            log.info("Setting gains from file {}".format(self.path_gain_file))
            self.loadCSVfile(self.path_gain_file, 'gains')
        #print(self.channels_enabled)
 
