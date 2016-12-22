import csv
import multiprocessing
from time import strftime, gmtime, sleep

from rtgraph.core.constants import Constants
from rtgraph.common.fileManager import FileManager
from rtgraph.common.logger import Logger as Log


TAG = "CSV"


class CSVProcess(multiprocessing.Process):
    """
    Process to store and export data to a file.
    """
    def __init__(self, filename=None, path=None, timeout=0.5):
        """
        Sets up the file to export the data as CSV.
        If filename is not specified, a default name based on time will be used.
        :param filename: Name of the file where data will be exported.
        :type filename: str.
        :param path: Path where data file will be saved.
        :type path: str.
        :param timeout: Time to wait after emptying the internal buffer before next write.
        :type timeout: float.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._store_queue = multiprocessing.Queue()
        self._csv = None
        self._file = None
        self._timeout = timeout

        if filename is None:
            filename = strftime(Constants.csv_default_filename, gmtime())
        self._file = self._create_file(filename, path=path)
        Log.i(TAG, "Process ready")

    def add(self, time, values):
        """
        Adds a new row to fhe exported data file.
        :param time: Timestamp for the row.
        :type time: float.
        :param values: Values to add in the row.
        :type values: float list.
        :return:
        """
        array = [time]
        for value in values:
            array.append(value)
        self._store_queue.put(array)

    def run(self):
        """
        Process will monitor the internal buffer to write data to the export file,
        and the process will loop again after timeout if more data is available.
        :return:
        """
        Log.i(TAG, "Process starting...")
        self._csv = csv.writer(self._file, delimiter=Constants.csv_delimiter, quoting=csv.QUOTE_MINIMAL)
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
        """
        Signals the process to stop storing data.
        :return:
        """
        Log.i(TAG, "Process finishing...")
        self._exit.set()

    @staticmethod
    def _create_file(filename, path=None, extension=Constants.csv_extension):
        """
        Creates the file to export the data.
        :param filename: Name of the file where data will be exported.
        :type filename: str.
        :param path: Path where data file will be saved.
        :type path: str.
        :param extension: Extension to give to the export file.
        :type extension: str.
        :return: Reference to the export file.
        """
        FileManager.create_dir(path)
        full_path = FileManager.create_file(filename, extension=extension, path=path)
        if not FileManager.file_exists(full_path):
            Log.i(TAG, "Storing in {}".format(full_path))
            return open(full_path, "a", newline='')
        return None
