#!/usr/bin/env python
from multiprocessing import Process, Event
import numpy as np
from time import time
import serial

# logging
from log import Log


class SerialProcess(Process):
    def __init__(self, queue):
        Process.__init__(self)
        self.exit = Event()
        # local variables
        self.ser = serial.Serial()
        self.queue = queue
        # logging
        self.log = Log('SerialProcess')

    def run(self):
        self.init_time = time()
        try:
            while self.ser.isOpen() and not self.exit.is_set():
                data = self.ser.readline().strip()
                try:
                    data = map(float, data.split(','))
                    self.queue.put([time() - self.init_time] + data)
                except:
                    pass
            return
        except:
            self.log.e("Exception in SerialProcess")
            raise
        finally:
            self.closePort()
            self.log.i("Finished SerialProcess normally")

    def openPort(self, port='/dev/ttyACM0', bd=115200):
        self.ser.port = port
        self.ser.baudrate = bd
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.rtscts = 1
        self.ser.timeout = 0.5

        if self.ser.isOpen():
            return False
        try:
            self.ser.open()
            self.ser.flushInput()
            self.log.i("Opened Serial port" + str(port))
            return True
        except:
            self.log.e("Failed to open Serial port " + str(port))
            return False

    def closePort(self):
        self.log.i("Exiting process...")
        self.exit.set()

if __name__ == "__main__":
    import os
    os.system("python main.py")

