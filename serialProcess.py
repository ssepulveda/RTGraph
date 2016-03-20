import multiprocessing
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

    @staticmethod
    def list_ports():
        return list_ports.comports()

    def get_ports(self):
        ports = []
        for port in self.list_ports():
            ports.append(port[0])
        return ports

    def get_ports_full(self):
        ports = []
        for port in self.list_ports():
            ports.append(port)
        return ports

    def is_port_available(self, port):
        for ports in self.list_ports():
            if ports[0] == port:
                return True
        return False

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
                timestamp = time.time()
                while not self.exit.is_set():
                    # http://eli.thegreenplace.net/2009/08/07/a-live-data-monitor-with-python-pyqt-and-pyserial/
                    data = self.s.read(1)
                    data += self.s.read(self.s.inWaiting())
                    if len(data) > 0:
                        self.queue.put((data, (time.time() - timestamp)))
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