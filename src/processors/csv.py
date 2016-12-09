import multiprocessing
import logging as log

from time import strftime, gmtime
import csv


class CSVProcess(multiprocessing.Process):
    def __init__(self, filename=None):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

        self.csv = None

        if filename is None:
            filename = strftime("data/%Y-%m-%d_%H-%M-%S.csv", gmtime())

        self.csv = self._create_file(filename)

        log.info("CSVProcess ready")

    def write_line(self, txt):
        self.csv.writerow(txt)

    @staticmethod
    def _create_file(filename):
        file = open(filename, "wb")
        return csv.writer(file)
