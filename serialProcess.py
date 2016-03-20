import multiprocessing
import logging as log
import serial
import time


class SerialProcess(multiprocessing.Process):
    def __init__(self, result_queue):
        self.queue = result_queue
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.s = serial.Serial()
        log.info("SerialProcess ready")

    def list_ports(self):
        return None

    def is_port_avaliable(self, port):
        return True

    def open_port(self, port, bd=115200, timeout=0.5):
        self.s.port = port
        self.s.baudrate = bd
        self.s.stopbits = serial.STOPBITS_ONE
        self.s.bytesize = serial.EIGHTBITS
        self.s.timeout = timeout
        return self.is_port_avaliable(self.s.port)

    def run(self):
        if not self.s.isOpen():
            self.s.open()
            log.info("Port opened")
            time.clock()
            while not self.exit.is_set():
                # http://eli.thegreenplace.net/2009/08/07/a-live-data-monitor-with-python-pyqt-and-pyserial/
                data = self.s.read(1)
                data += self.s.read(self.s.inWaiting())
                if len(data) > 0:
                    timestamp = time.clock()
                    self.queue.put((data, timestamp))
                log.debug(data)
            log.info("SerialProcess finished")
            self.s.close()
        else:
            log.warning("Port is not opened")

    def stop(self):
        log.info("SerialProcess finishing...")
        self.exit.set()
