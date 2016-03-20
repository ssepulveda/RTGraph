import multiprocessing
import sys
import logging as log
import logging.handlers
from serialProcess import SerialProcess

TIMEOUT = 1000


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
            while count < 5:
                if not result_queue.empty():
                    print(value)
                    value = result_queue.get(block=False)
                    count = value[1]
            sp.stop()
            sp.join()
        else:
            log.info("Port is not available")
    else:
        log.warning("No ports detected")


def start_logging():
    log_format = log.Formatter('%(asctime)s,%(levelname)s,%(message)s')
    logger = log.getLogger()
    logger.setLevel(log.INFO)

    file_handler = logging.handlers.RotatingFileHandler("RTGraph.log", maxBytes=1024, backupCount=3)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    console_handler = log.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)


def user_info():
    log.info("Platform %s", sys.platform)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    start_logging()
    user_info()

    log.info("Starting RTGraph")
    main()
    log.info("Finishing RTGraph")
    sys.exit()
