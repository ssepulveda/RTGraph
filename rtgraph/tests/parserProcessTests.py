import unittest
import numpy as np
from multiprocessing import Queue

from rtgraph.processors.Parser import ParserProcess
from rtgraph.core.constants import Constants


class ParserProcessTests(unittest.TestCase):
    def test_fast_consumer(self):
        parser, queue = self._create_parser()
        parser.start()
        parser.add([1, b'0\n'])
        self._stop_parser(parser)
        values = queue.get(False)
        self.assertEqual(float(0.0), values[1][0])

    def test_fast_consumer_string(self):
        parser, queue = self._create_parser()
        parser.start()
        parser.add([1, '0\n'])
        self._stop_parser(parser)
        values = queue.get(False)
        self.assertEqual(float(0.0), values[1][0])

    def test_random_data(self):
        result = []
        values, original_values = self._create_samples(99)
        parser, queue = self._create_parser()
        parser.start()

        for v in values:
            parser.add(v)
        self._stop_parser(parser)

        while not queue.empty():
            result.append(list(queue.get(False)))
        self.assertEqual(result, original_values)

    def _create_samples(self, samples):
        self.maxDiff = None
        data, original_data = self._create_random_values(samples)
        time = self._create_time_vector(0, samples)
        values = []
        original_values = []
        for idx in range(samples):
            values.append([time[idx], data[idx]])
            original_values.append([time[idx], [original_data[idx]]])
        return values, original_values

    @staticmethod
    def _create_parser():
        queue = Queue()
        parser = ParserProcess(queue)
        return parser, queue

    @staticmethod
    def _stop_parser(parser):
        parser.stop()
        parser.join(1000)

    @staticmethod
    def _create_random_values(samples, result_type=bytes):
        values = []
        original_values = []
        for v in np.random.rand(samples):
            if result_type == str:
                values.append("{}\n".format(v))
            elif result_type == bytes:
                values.append(str("{}\n".format(v)).encode(Constants.app_encoding))
            original_values.append(v)
        return values, original_values

    @staticmethod
    def _create_time_vector(minimun, maximum, step=None):
        if step is None:
            step = 1
        return np.arange(start=minimun, stop=maximum, step=step).tolist()


if __name__ == '__main__':
    unittest.main()
