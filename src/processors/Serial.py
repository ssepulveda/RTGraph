import multiprocessing
from time import time
import logging as log

import serial
from serial.tools import list_ports


class SerialProcess(multiprocessing.Process):
    def __init__(self, result_queue):
        self.queue = result_queue
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.s = serial.Serial()
        log.info("SerialProcess ready")

    def open_port(self, port, bd=115200, timeout=0.5):
        self.s.port = port
        self.s.baudrate = bd
        self.s.stopbits = serial.STOPBITS_ONE
        self.s.bytesize = serial.EIGHTBITS
        self.s.timeout = timeout
        return self.is_port_available(self.s.port)

    def run(self):
        if self.is_port_available(self.s.port):
            if not self.s.isOpen():
                self.s.open()
                log.info("Port opened")
                timestamp = time()
                while not self.exit.is_set():
                    """
                    http://eli.thegreenplace.net/2009/08/07/a-live-data-monitor-with-python-pyqt-and-pyserial/
                    """
                    data = self.s.read(1)
                    data += self.s.read(self.s.inWaiting())
                    if len(data) > 0:
                        self.queue.put((data, (time() - timestamp)))
                    log.debug(data)
                log.info("SerialProcess finished")
                self.s.close()
            else:
                log.warning("Port is not opened")
        else:
            log.warning("Port is not available")

    def stop(self):
        log.info("SerialProcess finishing...")
        self.exit.set()

    @staticmethod
    def get_serial_ports():
        found_ports = []
        for port in list(list_ports.comports()):
            log.debug("found device {}".format(port))
            found_ports.append(port[1])
        return found_ports

    @staticmethod
    def is_port_available(port):
        for p in list(list_ports.comports()):
            if p[1] == port:
                return True
        return False
