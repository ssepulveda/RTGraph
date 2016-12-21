import logging
import logging.handlers
import sys
from enum import Enum

from rtgraph.common.architecture import Architecture
from rtgraph.common.fileManager import FileManager
from rtgraph.core.constants import Constants


class Logger:
    def __init__(self, level, enable_console=False):
        """
        Constructor for Logger (wrapper of logging).
        Creates both console (stdout) logging and file logging (as csv).
        :param level: Level to show in log.
        :type level: int.
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
        logging.shutdown()

    @staticmethod
    def d(tag, msg):
        logging.debug("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def i(tag, msg):
        logging.info("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def w(tag, msg):
        logging.warning("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def e(tag, msg):
        logging.error("[{}] {}".format(str(tag), str(msg)))

    @staticmethod
    def _show_user_info():
        """
        Logs in info level architecture related information.
        :return:
        """
        tag = "User"
        Logger.i(tag, "Platform: {}".format(Architecture.get_os_name()))
        Logger.i(tag, "Path: {}".format(Architecture.get_path()))
        Logger.i(tag, "Python: {}".format(Architecture.get_python_version()))


class LoggerLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
