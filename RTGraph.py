import multiprocessing
import sys
import platform
import logging as log
import logging.handlers
import argparse
from serialProcess import SerialProcess
from gui import *

TIMEOUT = 1000


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    result_queue = multiprocessing.Queue()

    sp = SerialProcess(result_queue)
    ports = sp.get_ports()
    log.info(ports)
    if 0 < len(ports):
        sp.open_port(ports[0])
        if sp.is_port_available(ports[0]):
            sp.start()
            value = result_queue.get(block=True, timeout=TIMEOUT)
            count = 0
            while count < 1:
                if not result_queue.empty():
                    value = result_queue.get(block=False)
                    count = value[1]
            sp.stop()
            sp.join()
        else:
            log.info("Port is not available")
    else:
        log.warning("No ports detected")


def start_logging(level):
    log_format = log.Formatter('%(asctime)s,%(levelname)s,%(message)s')
    logger = log.getLogger()
    logger.setLevel(level)

    file_handler = logging.handlers.RotatingFileHandler("RTGraph.log", maxBytes=1024, backupCount=2)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    console_handler = log.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)


def user_info():
    log.info("Platform: %s", platform.platform())
    log.info("Path: %s", sys.path[0])
    log.info("Python: %s", sys.version[0:5])


def man():
    parser = argparse.ArgumentParser(description='RTGraph\nA real time plotting and logging application')
    parser.add_argument("-l", "--log",
                        dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the logging level")
    return parser


if __name__ == '__main__':
    multiprocessing.freeze_support()
    args = man().parse_args()
    if args.logLevel:
        start_logging(args.logLevel)
    else:
        start_logging(log.INFO)
    user_info()

    log.info("Starting RTGraph")

    # main()

    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    app.exec_()

    log.info("Finishing RTGraph")
    log.shutdown()
    sys.exit()
