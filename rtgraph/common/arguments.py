import argparse

from rtgraph.common.logger import Logger as Log
from rtgraph.common.logger import LoggerLevel

TAG = "Arguments"


class Arguments:
    def __init__(self):
        self._parser = None

    def create(self):
        """
        Creates and parses the arguments to be used by the application.
        :return:
        """
        parser = argparse.ArgumentParser(description='RTGraph\nA real time plotting and logging application')
        parser.add_argument("-i", "--info",
                            dest="log_level_info",
                            action='store_true',
                            help="Enable info messages"
                            )

        parser.add_argument("-v", "-d", "--debug",
                            dest="log_level_debug",
                            action='store_true',
                            help="Enable debug messages"
                            )

        parser.add_argument("-s", "--samples",
                            dest="user_samples",
                            default=500,
                            help="Specify number of sample to show on plot"
                            )
        self._parser = parser.parse_args()

    def set_user_log_level(self):
        """
        Sets the user specified log level.
        :return:
        """
        if self._parser is not None:
            self._parse_log_level()
        else:
            Log.w(TAG, "Parser was not created !")
            return None

    def get_user_samples(self):
        """
        Gets the user specified samples to show in the plot.
        :return: Samples specified by user, or default value if not specified.
        """
        return int(self._parser.user_samples)

    def _parse_log_level(self):
        """
        Sets the log level depending on user specification.
        :return:
        """
        if self._parser.log_level_info:
            Log(LoggerLevel.INFO)
        elif self._parser.log_level_debug:
            Log(LoggerLevel.DEBUG)
        else:
            Log(LoggerLevel.WARNING)
