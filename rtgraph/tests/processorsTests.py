import unittest
from multiprocessing import Queue
from rtgraph.processors.Parser import ParserProcess


class ProcessorsTests(unittest.TestCase):
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

    @staticmethod
    def _create_parser():
        queue = Queue()
        parser = ParserProcess(queue)
        return parser, queue

    @staticmethod
    def _stop_parser(parser):
        parser.stop()
        parser.join()


if __name__ == '__main__':
    unittest.main()
