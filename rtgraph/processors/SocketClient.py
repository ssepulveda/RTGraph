import multiprocessing
from time import time

import socket

from rtgraph.core.constants import Constants
from rtgraph.common.logger import Logger as Log


TAG = "Socket"


class SocketProcess(multiprocessing.Process):
    """
    Socket client
    """
    def __init__(self, parser_process):
        """
        Initialises values for process.
        :param parser_process: Reference to a ParserProcess instance.
        :type parser_process: ParserProcess
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._parser = parser_process
        self._socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Log.i(TAG, "Process Ready")

    def open(self, port='', speed=5555, timeout=0.01):
        """
        Opens a socket connection to specified host and port
        :param port: Host address to connect to.
        :type port: str.
        :param speed: Port number to connect to.
        :type speed: int.
        :param timeout: Sets timeout for socket interactions.
        :type timeout: float.
        :return: True if the connection was open.
        :rtype: bool.
        """
        try:
            #self._socket_client.timeout = timeout
            speed = int(speed)
            self._socket_client.connect((port, speed))
            Log.i(TAG, "Socket open {}:{}".format(port, speed))
            return True
        except socket.timeout:
            Log.w(TAG, "Connection timeout")
        return False

    def run(self):
        """
        Reads the socket until a stop call is made.
        :return:
        """
        Log.i(TAG, "Process starting...")
        timestamp = time()

        while not self._exit.is_set():
            stamp = time() - timestamp
            try:
                data = self._socket_client.recv(Constants.SocketClient.buffer_recv_size).decode()
                if len(data) > 0:
                    self._parser.add([stamp, data])
            except socket.timeout:
                Log.w(TAG, "read timeout")
        Log.i(TAG, "Process finished")

    def stop(self):
        """
        Signals the process to stop acquiring data.
        :return:
        """
        Log.i(TAG, "Process finishing...")
        self._socket_client.close()
        self._exit.set()

    @staticmethod
    def get_default_host():
        """
        Returns a list of local host names, localhost, host name and local ip address, if available.
        :return: str list.
        """
        values = socket.gethostbyaddr(socket.gethostname())
        hostname = values[0]
        hostip = values[2][0]

        if hostip is not None:
            return [Constants.SocketClient.host_default, hostname, hostip]
        else:
            return [Constants.SocketClient.host_default, hostname]

    @staticmethod
    def get_default_port():
        """
        Returns a list of commonly used socket ports.
        :return: str list.
        """
        return [str(v) for v in Constants.SocketClient.port_default]
