import unittest
from time import sleep

from rtgraph.core.worker import Worker
from rtgraph.core.constants import SourceType


class WorkerTests(unittest.TestCase):
    def test_one(self):
        time = 2
        speed = 0.02
        error = 0.8
        zeros = 0
        passed = False
        expected_samples = (time * (1/speed))
        samples_plus_error = (expected_samples / error)

        # Log(LoggerLevel.DEBUG, enable_console=True)
        worker = Worker(port=None,
                        speed=float(speed),
                        samples=int(samples_plus_error),
                        source=SourceType.simulator,
                        export_enabled=False)
        worker.start()
        sleep(time)
        worker.stop()
        worker.consume_queue()

        for v in worker.get_values_buffer(0):
            if v == 0:
                zeros += 1

        if 0 < zeros <= (samples_plus_error - expected_samples):
            passed = True
        self.assertTrue(passed)


if __name__ == '__main__':
    unittest.main()
