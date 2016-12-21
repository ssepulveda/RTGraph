import multiprocessing
from time import time

import serial
from serial.tools import list_ports

from rtgraph.common.architecture import Architecture
from rtgraph.common.architecture import OSType
from rtgraph.core.constants import Constants
from rtgraph.common.logger import Logger as Log


TAG = "Serial"


class SerialProcess(multiprocessing.Process):
    def __init__(self, parser_process):
        """
        Initialises values for process.
        :param parser_process: Reference to a ParserProcess instance.
        :type parser_process: ParserProcess.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._parser = parser_process
        self._serial = serial.Serial()
        Log.i(TAG, "Process ready")

    def open(self, port, speed=Constants.serial_default_speed, timeout=Constants.serial_timeout_ms):
        """
        Opens a specified serial port.
        :param port: Serial port name.
        :type port: basestring
        :param speed: Baud rate, in bps, to connect to port.
        :type speed: int
        :param timeout: Sets the general connection timeout.
        :type timeout: float
        :return: True if the port is available.
        """
        self._serial.port = port
        self._serial.baudrate = int(speed)
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = timeout
        return self._is_port_available(self._serial.port)

    def run(self):
        """
        Reads the serial port expecting CSV until a stop call is made.
        The expected format is comma (",") separated values, and a new line (CRLF or LF) as a new row.
        While running, it will parse CSV data convert each value to float and added to a queue.
        If incoming data from serial port can't be converted to float, that data will be discarded.
        :return:
        """
        Log.i(TAG, "Process starting...")
        if self._is_port_available(self._serial.port):
            if not self._serial.isOpen():
                self._serial.open()
                Log.i(TAG, "Port opened")
                timestamp = time()
                while not self._exit.is_set():
                    self._parser.add([time() - timestamp, self._serial.readline()])
                Log.i(TAG, "Process finished")
                self._serial.close()
            else:
                Log.w(TAG, "Port is not opened")
        else:
            Log.w(TAG, "Port is not available")

    def stop(self):
        """
        Signals the process to stop acquiring data.
        :return:
        """
        Log.i(TAG, "Process finishing...")
        self._exit.set()

    @staticmethod
    def get_ports():
        """
        Gets a list of the available serial ports.
        :return: List of available serial ports.
        """
        if Architecture.get_os() is OSType.macosx:
            import glob
            return glob.glob("/dev/tty.*")
        else:
            found_ports = []
            for port in list(list_ports.comports()):
                Log.d(TAG, "found device {}".format(port))
                found_ports.append(port.device)
            return found_ports

    @staticmethod
    def get_speeds():
        """
        Gets a list of the common serial baud rates, in bps.
        :return: List of the common baud rates, in bps.
        """
        return [str(v) for v in [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]]

    def _is_port_available(self, port):
        """
        Checks is the port is currently connected to the host.
        :param port: Port name to be verified.
        :return: True if the port is connected to the host.
        """
        for p in self.get_ports():
            if p == port:
                return True
        return False
