import multiprocessing
from time import sleep

from common.logger import Logger as Log


TAG = "Parser"


class ParserProcess(multiprocessing.Process):
    def __init__(self, result_queue, split=",", timeout=0.05):
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._in_queue = multiprocessing.Queue()
        self._out_queue = result_queue
        self._timeout = timeout
        self._split = split
        Log.d(TAG, "Process ready")

    def add(self, txt):
        self._in_queue.put(txt)

    def run(self):
        Log.d(TAG, "Process starting...")
        while not self._exit.is_set():
            while not self._in_queue.empty():
                queue = self._in_queue.get(timeout=self._timeout)
                self._parse_csv(queue[0], queue[1])
            sleep(self._timeout)
        Log.d(TAG, "Process finished")

    def stop(self):
        Log.d(TAG, "Process finishing...")
        self._exit.set()

    def _parse_csv(self, time, line):
        if len(line) > 0:
            try:
                values = line.decode("UTF-8").split(self._split)
                values = [float(v) for v in values]
                Log.d(TAG, values)
                self._out_queue.put((time, values))
            except:
                Log.w(TAG, "Wrong format? raw: {}".format(line.strip()))

