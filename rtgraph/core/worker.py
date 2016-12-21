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
    def __init__(self,
                 port=None,
                 speed=Constants.serial_default_speed,
                 samples=Constants.argument_default_samples,
                 source=SourceType.serial,
                 export_enabled=False,
                 export_path=Constants.app_export_path):
        self._data_buffers = None
        self._time_buffer = None
        self._acquisition_process = None
        self._parser_process = None
        self._csv_process = None
        self.lines = 0
        self.queue = Queue()
        self._port = port
        self._spped = float(speed)
        self._samples = samples
        self._source = source
        self._export = export_enabled
        self._path = export_path

    def start(self):
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
        if self._acquisition_process.open(port=self._port, speed=self._spped):
            self._parser_process.start()
            if self._export:
                self._csv_process.start()
            self._acquisition_process.start()
            return True
        else:
            Log.i(TAG, "Port is not available")
            return False

    def stop(self):
        if self._acquisition_process is not None and self._acquisition_process.is_alive():
            self._acquisition_process.stop()
            self._acquisition_process.join(Constants.process_join_timeout_ms)

        if self._parser_process is not None and self._parser_process.is_alive():
            self._parser_process.stop()
            self._parser_process.join(Constants.process_join_timeout_ms)

        if self._csv_process is not None and self._csv_process.is_alive():
            self._csv_process.stop()
            self._csv_process.join(Constants.process_join_timeout_ms)

    def add_time(self, time):
        self._time_buffer.append(time)

    def add_values(self, values):
        # detect how many lines are present to plot
        size = len(values)
        if self.lines < size:
            if size > len(Constants.plot_colors):
                self.lines = len(Constants.plot_colors)
            else:
                self.lines = size

        # store the data in respective buffers
        for idx in range(self.lines):
            self._data_buffers[idx].append(values[idx])

    def get_time_buffer(self):
        return self._time_buffer.get_all()

    def get_values_buffer(self, idx=0):
        return self._data_buffers[idx].get_all()

    def get_lines(self):
        return self.lines

    def is_running(self):
        return self._acquisition_process is not None and self._acquisition_process.is_alive()

    @staticmethod
    def get_source_ports(source):
        if source == SourceType.serial:
            return SerialProcess.get_ports()
        elif source == SourceType.simulator:
            return SimulatorProcess.get_ports()
        else:
            Log.w(TAG, "Unknown source selected")
            return None

    @staticmethod
    def get_source_speeds(source):
        if source == SourceType.serial:
            return SerialProcess.get_speeds()
        elif source == SourceType.simulator:
            return SimulatorProcess.get_speeds()
        else:
            Log.w(TAG, "Unknown source selected")
            return None

    def reset_buffers(self, samples):
        """
        Set up/clear the internal buffers used to store and display the signals.
        :param samples: number of samples to set.
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
