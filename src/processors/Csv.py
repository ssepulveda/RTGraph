import multiprocessing
import logging as log

from time import strftime, gmtime
import csv
import os.path


class CSVProcess(multiprocessing.Process):
    def __init__(self, queue, lock, filename=None, path=None):
        multiprocessing.Process.__init__(self)

        self._csv = None
        self._file = None
        self.queue = queue
        self._lock = lock

        if filename is None:
            filename = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

        self._file = self._create_file(filename, path=path)

        log.info("CSVProcess ready")

    def start(self):
        self._write_queue()

    def _write_queue(self):
        self._set_lock()
        self._csv = csv.writer(self._file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        while not self.queue.empty():
            tmp = self.queue.get()
            if tmp is not None:
                self._csv.writerow(tmp)
        self._close_file()
        self._set_lock(False)
        return True

    @staticmethod
    def _create_file(filename, path=None, extension="csv"):
        if path is not None:
            if os.path.isdir(path):
                os.makedirs(path)

        if path is None:
            full_path = str("{}.{}".format(filename, extension))
        else:
            full_path = str("{}/{}.{}".format(path, filename, extension))

        return open(full_path, "a", newline='')

    def _close_file(self):
        self._file.close()

    def _set_lock(self, locked=True):
        if locked:
            self._lock.acquire()
        else:
            self._lock.release()


