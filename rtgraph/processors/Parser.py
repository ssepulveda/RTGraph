import multiprocessing
from time import sleep

from rtgraph.core.constants import Constants
from rtgraph.common.logger import Logger as Log


TAG = "Parser"


class ParserProcess(multiprocessing.Process):
    """
    Process to parse incoming data, parse it, and then distribute it to graph and storage.
    """
    def __init__(self, data_queue, store_reference=None,
                 split=Constants.csv_delimiter,
                 timeout=Constants.parser_timeout_ms):
        """

        :param data_queue: Reference to Queue where processed data will be put.
        :type data_queue: multiprocessing Queue.
        :param store_reference: Reference to CSVProcess instance, if needed.
        :type store_reference: CSVProcess (multiprocessing.Process)
        :param split: Delimiter in incoming data.
        :type split: str.
        :param timeout: Time to wait after emptying the internal buffer before next parsing.
        :type timeout: float.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._in_queue = multiprocessing.Queue()
        self._out_queue = data_queue
        self._timeout = timeout
        self._split = split
        self._store_reference = store_reference
        Log.d(TAG, "Process ready")

    def add(self, txt):
        """
        Adds new raw data to internal buffer.
        :param txt: Raw data comming from acquisition process.
        :type txt: basestring.
        :return:
        """
        self._in_queue.put(txt)

    def run(self):
        """
        Process will monitor the internal buffer to parse raw data and distribute to graph and storage, if needed.
        The process will loop again after timeout if more data is available.
        :return:
        """
        Log.d(TAG, "Process starting...")
        while not self._exit.is_set():
            self._consume_queue()
            sleep(self._timeout)
        # last check on the queue to completely remove data.
        self._consume_queue()
        Log.d(TAG, "Process finished")

    def stop(self):
        """
        Signals the process to stop parsing data.
        :return:
        """
        Log.d(TAG, "Process finishing...")
        self._exit.set()

    def _consume_queue(self):
        """
        Consumer method for the queues/process.
        Used in run method to recall after a stop is requested, to ensure queue is emptied.
        :return:
        """
        while not self._in_queue.empty():
            queue = self._in_queue.get(timeout=self._timeout)
            self._parse_csv(queue[0], queue[1])

    def _parse_csv(self, time, line):
        """
        Parses incoming data and distributes to external processes.
        :param time: Timestamp.
        :type time: float.
        :param line: Raw data coming from acquisition process.
        :type line: basestring.
        :return:
        """
        if len(line) > 0:
            try:
                if type(line) == bytes:
                    values = line.decode("UTF-8").split(self._split)
                elif type(line) == str:
                    values = line.split(self._split)
                else:
                    raise TypeError
                values = [float(v) for v in values]
                Log.d(TAG, values)
                self._out_queue.put((time, values))
                if self._store_reference is not None:
                    self._store_reference.add(time, values)
            except ValueError:
                Log.w(TAG, "Can't convert to float. Raw: {}".format(line.strip()))
            except AttributeError:
                Log.w(TAG, "Attribute error on type ({}). Raw: {}".format(type(line), line.strip()))

