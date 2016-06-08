import multiprocessing
import logging as log
import io
import time
import subprocess

class PipeProcess(multiprocessing.Process):
    def __init__(self, result_queue,
                 cmd="./fake_acq.py", args=[]):
        self.queue = result_queue
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.cmd = cmd
        self.args = args
        log.info("PipeProcess ready")

    # Run is started in the new process
    def run(self):
        timestamp = time.time()
        proc = subprocess.Popen([self.cmd,  ] + self.args,
                                stdout=subprocess.PIPE,
                                universal_newlines=True,
                                bufsize=1)
        for line in proc.stdout:
            """io.TextIOWrapper(proc.stdout, 
                                     line_buffering=False,
                                     write_through=True,
                                     encoding=None):
            """
            if self.exit.is_set():
                proc.terminate()

            # Parse and push
            data = line.split("\t")
            
            if len(data) > 1:
                # data is (event Number, timestamp, [SIZE ADC values])
                vals = list(map(int, data[2:-1]))
                print("Got data: {}".format(' '.join([str(k) for k in vals])))
                self.queue.put((int(data[0]),int(data[1]),vals))

            else:
                continue

    def stop(self):
        log.info("PipeProcess finishing...")
        self.exit.set()
