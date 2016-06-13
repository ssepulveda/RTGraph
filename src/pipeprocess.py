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
        with subprocess.Popen([self.cmd,  ] + self.args,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                universal_newlines=True,
                                bufsize=1) as proc:
            for line in proc.stdout:
                """io.TextIOWrapper(proc.stdout, 
                                        line_buffering=False,
                                        write_through=True,
                                        encoding=None):
                """
                if self.exit.is_set():
                    #proc.stdin.write("\n")
                    #proc.stdin.flush()
                    proc.terminate()

                data = line.strip()
                if data != '':
                    self.queue.put(data)

    def stop(self):
        log.info("PipeProcess finishing...")
        self.exit.set()
