import logging as log
import logging.handlers
import sys

from common.architecture import Architecture


class Logger:
    def __init__(self, level):
        log_format = log.Formatter('%(asctime)s,%(levelname)s,%(message)s')
        logger = log.getLogger()
        logger.setLevel(level)

        file_handler = logging.handlers.RotatingFileHandler("RTGraph.log", maxBytes=(10240 * 5), backupCount=0)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        console_handler = log.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        _show_user_info()


def _show_user_info():
    log.info("Platform: %s", Architecture.get_os_string())
    log.info("Path: %s", Architecture.get_path())
    log.info("Python: %s", Architecture.get_python_version())
