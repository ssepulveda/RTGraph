import logging
import logging.handlers
import sys
from enum import Enum

from rtgraph.common.architecture import Architecture
from rtgraph.common.fileManager import FileManager
from rtgraph.core.constants import Constants


class Logger:
    """
    Wrapper for logging package.
    """
    def __init__(self, level, enable_console=False):
        """
        Creates file logging (as csv) and to console, if requested.
        :param level: Level to show in log.
        :type level: int.
        :param enable_console: Enabled logging to console.
        :type enable_console: bool,
        """
        log_format_file = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s')
        log_format_console = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(level.value)

        FileManager.create_dir(Constants.app_export_path)
        file_handler = logging.handlers.RotatingFileHandler("{}/{}"
                                                            .format(Constants.app_export_path, Constants.log_filename),
                                                            maxBytes=Constants.log_max_bytes,
                                                            backupCount=0)
        file_handler.setFormatter(log_format_file)
        self.logger.addHandler(file_handler)

        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(log_format_console)
            self.logger.addHandler(console_handler)

        self._show_user_info()

    @staticmethod
    def close():
        """
        Closes the enabled loggers.
        :return:
        """
        logging.shutdown()

    @staticmethod
    def d(tag, msg):
        """
        Logs at debug level.
        :param tag: TAG to identify the log.
        :type tag: str.
        :param msg: Message to log.
        :type msg: str.
        :return:
        """
        logging.debug("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def i(tag, msg):
        """
        Logs at info level.
        :param tag: TAG to identify the log.
        :type tag: str.
        :param msg: Message to log.
        :type msg: str.
        :return:
        """
        logging.info("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def w(tag, msg):
        """
        Logs at warning level.
        :param tag: TAG to identify the log.
        :type tag: str.
        :param msg: Message to log.
        :type msg: str.
        :return:
        """
        logging.warning("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def e(tag, msg):
        """
        Logs at error level.
        :param tag: TAG to identify the log.
        :type tag: str.
        :param msg: Message to log.
        :type msg: str.
        :return:
        """
        logging.error("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def _show_user_info():
        """
        Logs at info level architecture related information.
        :return:
        """
        tag = "User"
        Logger.i(tag, "Platform: {}".format(Architecture.get_os_name()))
        Logger.i(tag, "Path: {}".format(Architecture.get_path()))
        Logger.i(tag, "Python: {}".format(Architecture.get_python_version()))


class LoggerLevel(Enum):
    """
    Enum for the Logger levels (wrappers for logging package levels).
    """
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
