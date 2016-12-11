import multiprocessing
from PyQt4 import QtGui

from ui import mainWindow
from common.argParser import *
from common.architecture import Architecture

MINIMAL_PYTHON_VERSION_MAJOR = 3
MINIMAL_PYTHON_VERSION_MINOR = 2


if __name__ == '__main__':
    if Architecture.is_python_version(MINIMAL_PYTHON_VERSION_MAJOR, minor=MINIMAL_PYTHON_VERSION_MINOR):
        multiprocessing.freeze_support()
        args = ArgParser()
        args.create()
        args.parse()

        log.info("Starting RTGraph")
        app = QtGui.QApplication(sys.argv)
        win = mainWindow.MainWindow(port=args.get_user_port(),
                                    bd=args.get_user_bd(),
                                    samples=args.get_user_samples()
                                    )
        win.show()
        app.exec()

        log.info("Finishing RTGraph\n")
        log.shutdown()
        win.close()
        app.exit()
        sys.exit()
    else:
        print("RTGraph requires Python {}.{} to run"
              .format(MINIMAL_PYTHON_VERSION_MAJOR, MINIMAL_PYTHON_VERSION_MINOR))
        exit(1)
