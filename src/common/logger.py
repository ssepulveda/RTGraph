import logging as log
import logging.handlers
import sys

from common.architecture import Architecture


class Logger:
    def __init__(self, level):
        """
        Constructor for Logger (wrapper of logging).
        Creates both console (stdout) logging and file logging (as csv).
        :param level: Level to show in log.
        :type level: int.
        """
        log_format_file = log.Formatter('%(asctime)s,%(levelname)s,%(message)s')
        log_format_console = log.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger = log.getLogger()
        logger.setLevel(level)

        file_handler = logging.handlers.RotatingFileHandler("RTGraph.log", maxBytes=(10240 * 5), backupCount=0)
        file_handler.setFormatter(log_format_file)
        logger.addHandler(file_handler)

        console_handler = log.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format_console)
        logger.addHandler(console_handler)

        self._show_user_info()

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
    def _show_user_info():
        """
        Logs in info level architecture related information.
        :return:
        """
        log.info("Platform: %s", Architecture.get_os_name())
        log.info("Path: %s", Architecture.get_path())
        log.info("Python: %s", Architecture.get_python_version())
