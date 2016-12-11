import multiprocessing
import logging as log

from time import strftime, gmtime
import csv
import os.path


class CSVProcess(multiprocessing.Process):
    def __init__(self, queue, lock, filename=None, path=None):
        multiprocessing.Process.__init__(self)

        self.CSV = None
        self.file = None
        self.queue = queue
        self.lock = lock

        if filename is None:
            filename = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

        self.file = self.__create_file(filename, path=path)

        log.info("CSVProcess ready")

    def start(self):
        self.__write_queue()

    def __write_queue(self):
        self.__set_lock()
        self.CSV = csv.writer(self.file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        while not self.queue.empty():
            tmp = self.queue.get()
            if tmp is not None:
                self.CSV.writerow(tmp)
        self.__close_file()
        self.__set_lock(False)
        return True

    @staticmethod
    def __create_file(filename, path=None, extension="csv"):
        if path is not None:
            if os.path.isdir(path):
                os.makedirs(path)

        if path is None:
            full_path = str("{}.{}".format(filename, extension))
        else:
            full_path = str("{}/{}.{}".format(path, filename, extension))

        return open(full_path, "a", newline='')

    def __close_file(self):
        self.file.close()

    def __set_lock(self, locked=True):
        if locked:
            self.lock.acquire()
        else:
            self.lock.release()


