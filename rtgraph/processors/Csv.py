import csv
import multiprocessing
import os.path
from time import strftime, gmtime, sleep

from rtgraph.common.logger import Logger as Log

TAG = "CSV"


class CSVProcess(multiprocessing.Process):
    def __init__(self, filename=None, path=None, timeout=0.5):
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._store_queue = multiprocessing.Queue()
        self._csv = None
        self._file = None
        self._timeout = timeout

        if filename is None:
            filename = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

        self._file = self._create_file(filename, path=path)

        Log.i(TAG, "Process ready")

    def add(self, time, values):
        array = [time]
        for value in values:
            array.append(value)
        self._store_queue.put(array)

    def run(self):
        Log.i(TAG, "Process starting...")
        self._csv = csv.writer(self._file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        while not self._exit.is_set():
            if not self._store_queue.empty():
                while not self._store_queue.empty():
                    data = self._store_queue.get(timeout=self._timeout/10)
                    if data is not None:
                        self._csv.writerow(data)
            sleep(self._timeout)
        Log.i(TAG, "Process finished")
        self._file.close()

    def stop(self):
        Log.i(TAG, "Process finishing...")
        self._exit.set()

    @staticmethod
    def _create_file(filename, path=None, extension="csv"):
        if path is not None:
            if not os.path.isdir(path):
                os.makedirs(path)

        if path is None:
            full_path = str("{}.{}".format(filename, extension))
        else:
            full_path = str("{}/{}.{}".format(path, filename, extension))
        Log.i(TAG, "Storing in {}".format(full_path))
        return open(full_path, "a", newline='')
