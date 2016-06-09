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
        self.num_sensors = 8*1 # for VATA64 front-end
        self.num_integrations = 100
        
        self.integrate = False # no integration mode
        self.queue = multiprocessing.Queue()
        
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
        colors = [pg.intColor(200, alpha=k) for k in intensity/ np.max(intensity) * 100] 
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
        
        # update num_sensors
        self.num_sensors = len(self.sensor_ids)
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
    
