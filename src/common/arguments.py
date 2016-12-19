import argparse
from common.logger import *


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

        parser.add_argument("-p", "--port",
                            dest="user_port",
                            default=None,
                            help="Specify serial port to use"
                            )

        parser.add_argument("-b", "--baudrate",
                            dest="user_bd",
                            default=115200,
                            help="Specify serial port baudrate to use"
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
            log.warning("Parser was not created !")
            return None

    def get_user_port(self):
        """
        Gets the user specified port name.
        :return: Port name, if specified by user.
        """
        if self._parser.user_port is None:
            return None
        else:
            return str(self._parser.user_port)

    def get_user_bd(self):
        """
        Gets the user specified baud rate.
        :return: Baud rate specified by user, or default value if not specified.
        """
        return int(self._parser.user_bd)

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
            Logger(log.INFO)
        elif self._parser.log_level_debug:
            Logger(log.DEBUG)
        else:
            Logger(log.WARNING)
