import multiprocessing
from time import time
from time import sleep
import logging as log

import numpy as np


class SimulatorProcess(multiprocessing.Process):
    def __init__(self, result_queue):
        """
        Initialises values for process.
        :param result_queue: A queue where the obtained data will be appended.
        :type result_queue: multiprocessing queue
        """
        multiprocessing.Process.__init__(self)
        self._result_queue = result_queue
        self._exit = multiprocessing.Event()
        self._period = None
        log.info("Simulator ready")

    def open(self, port=None, speed=0.002, timeout=0.5):
        """
        Opens a specified serial port.
        :param port: Not used.
        :type port: basestring
        :param speed: Period of the generated signal.
        :type speed: float
        :param timeout: Not used.
        :type timeout: float
        :return: True if the port is available.
        """
        self._period = float(speed)
        log.info("Using sample rate at {}".format(self._period))
        return True

    def run(self):
        """
        Reads the serial port expecting CSV until a stop call is made.
        The expected format is comma (",") separated values, and a new line (CRLF or LF) as a new row.
        While running, it will parse CSV data convert each value to float and added to a queue.
        If incoming data from serial port can't be converted to float, that data will be discarded.
        :return:
        """
        timestamp = time()
        sin_coef = 2 * np.pi
        while not self._exit.is_set():
            stamp = time() - timestamp
            data = [np.sin(sin_coef * stamp)]
            log.debug(data)
            self._result_queue.put((stamp, data))
            sleep(self._period)
        log.info("Simulator finished")

    def stop(self):
        """
        Signals the process to stop acquiring data.
        :return:
        """
        log.info("Simulator finishing...")
        self._exit.set()

    @staticmethod
    def get_ports():
        """
        Gets a list of the available serial ports.
        :return: List of available serial ports.
        """
        return ["Simulator"]

    @staticmethod
    def get_speeds():
        """
        Gets a list of the common serial baud rates, in bps.
        :return: List of the common baud rates, in bps.
        """
        return [str(v) for v in [0.002, 0.004, 0.005, 0.010, 0.020, 0.050, 0.100, 0.250]]
