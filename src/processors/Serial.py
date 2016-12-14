import multiprocessing
from time import time
import logging as log

from common.architecture import Architecture
from common.architecture import OSType

import serial
from serial.tools import list_ports


class SerialProcess(multiprocessing.Process):
    def __init__(self, result_queue):
        multiprocessing.Process.__init__(self)
        self._result_queue = result_queue
        self._exit = multiprocessing.Event()
        self._serial = serial.Serial()
        log.info("SerialProcess ready")

    def open_port(self, port, bd=115200, timeout=0.5):
        self._serial.port = port
        self._serial.baudrate = bd
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = timeout
        return self._is_port_available(self._serial.port)

    def run(self):
        if self._is_port_available(self._serial.port):
            if not self._serial.isOpen():
                self._serial.open()
                log.info("Port opened")
                timestamp = time()
                while not self._exit.is_set():
                    data = self._serial.readline()
                    if len(data) > 0:
                        try:
                            values = data.decode("UTF-8").split(",")
                            values = [float(v) for v in values]
                            self._result_queue.put(((time() - timestamp), values))
                        except:
                            log.warn("Wrong format? {}".format(data))
                    log.debug(data)
                log.info("SerialProcess finished")
                self._serial.close()
            else:
                log.warning("Port is not opened")
        else:
            log.warning("Port is not available")

    def stop(self):
        log.info("SerialProcess finishing...")
        self._exit.set()

    @staticmethod
    def get_serial_ports():
        if Architecture.get_os() is OSType.macosx:
            import glob
            return glob.glob("/dev/tty.*")
        else:
            found_ports = []
            for port in list(list_ports.comports()):
                log.debug("found device {}".format(port))
                found_ports.append(port.device)
            return found_ports

    @staticmethod
    def get_serial_ports_speeds():
        return [str(v) for v in [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]]

    def _is_port_available(self, port):
        for p in self.get_serial_ports():
            if p == port:
                return True
        return False
