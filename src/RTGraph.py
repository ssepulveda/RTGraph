import multiprocessing
from PyQt4 import QtGui

from ui import mainWindow
from common.arguments import *
from common.architecture import Architecture

MINIMAL_PYTHON_VERSION_MAJOR = 3
MINIMAL_PYTHON_VERSION_MINOR = 2


if __name__ == '__main__':
    multiprocessing.freeze_support()
    args = Arguments()
    args.create()
    args.set_user_log_level()

    app = QtGui.QApplication(sys.argv)
    if Architecture.is_python_version(MINIMAL_PYTHON_VERSION_MAJOR, minor=MINIMAL_PYTHON_VERSION_MINOR):
        log.info("Starting RTGraph")
        win = mainWindow.MainWindow(port=args.get_user_port(),
                                    bd=args.get_user_bd(),
                                    samples=args.get_user_samples())
        win.show()
        app.exec()

        log.info("Finishing RTGraph\n")
        win.close()
    else:
        txt = str("RTGraph requires Python {}.{} to run"
                  .format(MINIMAL_PYTHON_VERSION_MAJOR, MINIMAL_PYTHON_VERSION_MINOR))
        log.error(txt)

    app.exit()
    log.shutdown()
    sys.exit()
