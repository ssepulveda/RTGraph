import multiprocessing
from time import time

from common.logger import Logger as Log
from common.architecture import Architecture
from common.architecture import OSType

import serial
from serial.tools import list_ports


TAG = "Serial"


class SerialProcess(multiprocessing.Process):
    def __init__(self, result_queue):
        """
        Initialises values for process.
        :param result_queue: A queue where the obtained data will be appended.
        :type result_queue: multiprocessing queue
        """
        multiprocessing.Process.__init__(self)
        self._result_queue = result_queue
        self._exit = multiprocessing.Event()
        self._serial = serial.Serial()
        Log.i(TAG, "Process ready")

    def open(self, port, speed=115200, timeout=0.5):
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
                    data = self._serial.readline()
                    Log.d(TAG, data)
                    if len(data) > 0:
                        try:
                            values = data.decode("UTF-8").split(",")
                            values = [float(v) for v in values]
                            self._result_queue.put(((time() - timestamp), values))
                        except:
                            Log.w(TAG, "Wrong format? {}".format(data))
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
