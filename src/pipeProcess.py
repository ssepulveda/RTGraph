import multiprocessing
import logging as log
import io
import time
import random
import subprocess

class PipeProcess(multiprocessing.Process):
    def __init__(self, result_queue, 
                 cmd="./fake_acq.py", args=""):
        self.queue = result_queue
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.cmd = cmd
        self.args = args
        log.info("PipeProcess ready")

    # Run is started in the new process
    def run(self):
        timestamp = time.time()
        proc = subprocess.Popen([self.cmd, self.args], stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            if self.exit.is_set():
                proc.terminate()
            
            # Parse and push
            data = line.split("\t")
            if len(data) > 1:
                vals = list(map(int, data[1:-1]))
                self.queue.put((int(data[0]),vals))

            else:
                continue

    def stop(self):
        log.info("PipeProcess finishing...")
        self.exit.set()
