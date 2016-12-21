from multiprocessing import Queue

from rtgraph.core.constants import Constants, SourceType
from rtgraph.core.ringBuffer import RingBuffer
from rtgraph.processors.Csv import CSVProcess
from rtgraph.processors.Parser import ParserProcess
from rtgraph.processors.Serial import SerialProcess
from rtgraph.processors.Simulator import SimulatorProcess
from rtgraph.common.logger import Logger as Log


TAG = "Worker"


class Worker:
    """
    Concentrates all workers (processes) to run the application.
    """
    def __init__(self,
                 port=None,
                 speed=Constants.serial_default_speed,
                 samples=Constants.argument_default_samples,
                 source=SourceType.serial,
                 export_enabled=False,
                 export_path=Constants.app_export_path):
        """
        Creates and orchestrates all processes involved in data acquisition, processing and storing.
        :param port: Port to open on start.
        :type port: basestring.
        :param speed: Speed for the specified port (depending on source).
        :type speed: float.
        :param samples: Number of samples to keep in the buffers (should match with plot samples).
        :type samples: int.
        :param source: Source type where data should be obtained
        :type source: SourceType.
        :param export_enabled: If true, data will be stored or exported in a file.
        :type export_enabled: bool.
        :param export_path: If specified, defines where the data will be exported.
        :type export_path: basestring.
        """
        self.queue = Queue()
        self._data_buffers = None
        self._time_buffer = None
        self._lines = 0

        self._acquisition_process = None
        self._parser_process = None
        self._csv_process = None

        self._port = port
        self._speed = float(speed)
        self._samples = samples
        self._source = source
        self._export = export_enabled
        self._path = export_path

    def start(self):
        """
        Starts all processes, based on configuration given in constructor.
        :return:
        """
        self.reset_buffers(self._samples)
        if self._export:
            self._csv_process = CSVProcess(path=self._path)
            self._parser_process = ParserProcess(self.queue, store_reference=self._csv_process)
        else:
            self._parser_process = ParserProcess(self.queue)

        if self._source == SourceType.serial:
            self._acquisition_process = SerialProcess(self._parser_process)
        elif self._source == SourceType.simulator:
            self._acquisition_process = SimulatorProcess(self._parser_process)
        if self._acquisition_process.open(port=self._port, speed=self._speed):
            self._parser_process.start()
            if self._export:
                self._csv_process.start()
            self._acquisition_process.start()
            return True
        else:
            Log.i(TAG, "Port is not available")
            return False

    def stop(self):
        """
        Stops all running processes.
        :return:
        """
        for process in [self._acquisition_process, self._parser_process, self._csv_process]:
            if process is not None and process.is_alive():
                process.stop()
                process.join(Constants.process_join_timeout_ms)

    def add_time(self, time):
        """
        Adds time data to internal time buffer.
        :param time: Time value to add to internal buffer.
        :type time: float.
        :return:
        """
        self._time_buffer.append(time)

    def add_values(self, values):
        """
        Adds value data to internal data buffer.
        :param values: values to add to internal buffers.
        :type values: float list.
        :return:
        """
        # detect how many lines are present to plot
        size = len(values)
        if self._lines < size:
            if size > len(Constants.plot_colors):
                self._lines = len(Constants.plot_colors)
            else:
                self._lines = size

        # store the data in respective buffers
        for idx in range(self._lines):
            self._data_buffers[idx].append(values[idx])

    def get_time_buffer(self):
        """
        Gets the complete buffer for time.
        :return: Time buffer.
        :rtype: float list.
        """
        return self._time_buffer.get_all()

    def get_values_buffer(self, idx=0):
        """
        Gets the complete buffer for a line data, depending on specified index.
        :param idx: Index of the line data to get.
        :type idx: int.
        :return: float list.
        """
        return self._data_buffers[idx].get_all()

    def get_lines(self):
        """
        Gets the current number of found lines in input data.
        :return: Current number of lines.
        :rtype: int.
        """
        return self._lines

    def is_running(self):
        """
        Checks if processes are running.
        :return: True if a process is running.
        :rtype: bool.
        """
        return self._acquisition_process is not None and self._acquisition_process.is_alive()

    @staticmethod
    def get_source_ports(source):
        """
        Gets the available ports for specified source.
        :param source: Source to get available ports.
        :type source: SourceType.
        :return: List of available ports.
        :rtype: basestring list.
        """
        if source == SourceType.serial:
            return SerialProcess.get_ports()
        elif source == SourceType.simulator:
            return SimulatorProcess.get_ports()
        else:
            Log.w(TAG, "Unknown source selected")
            return None

    @staticmethod
    def get_source_speeds(source):
        """
        Gets the available speeds for specified source.
        :param source: Source to get available speeds.
        :type source: SourceType.
        :return: List of available speeds.
        :rtype: basestring list.
        """
        if source == SourceType.serial:
            return SerialProcess.get_speeds()
        elif source == SourceType.simulator:
            return SimulatorProcess.get_speeds()
        else:
            Log.w(TAG, "Unknown source selected")
            return None

    def reset_buffers(self, samples):
        """
        Setup/clear the internal buffers.
        :param samples: Number of samples for the buffers.
        :type samples: int.
        :return:
        """
        self._data_buffers = []
        for tmp in Constants.plot_colors:
            self._data_buffers.append(RingBuffer(samples))
        self._time_buffer = RingBuffer(samples)
        while not self.queue.empty():
            self.queue.get()
        Log.i(TAG, "Buffers cleared")
