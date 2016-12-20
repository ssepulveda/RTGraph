import multiprocessing
from PyQt4 import QtGui

from ui import mainWindow
from common.arguments import *
from common.architecture import Architecture

MINIMAL_PYTHON_VERSION_MAJOR = 3
MINIMAL_PYTHON_VERSION_MINOR = 2


def _init_logger():
    args = Arguments()
    args.create()
    args.set_user_log_level()
    return args


def _start_app(app, args):
    log.info("Starting RTGraph")
    win = mainWindow.MainWindow(samples=args.get_user_samples())
    win.show()
    app.exec()

    log.info("Finishing RTGraph\n")
    win.close()


def _fail_app():
    txt = str("RTGraph requires Python {}.{} to run"
              .format(MINIMAL_PYTHON_VERSION_MAJOR, MINIMAL_PYTHON_VERSION_MINOR))
    log.error(txt)


def _close_app():
    log.shutdown()
    sys.exit()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    args = _init_logger()

    app = QtGui.QApplication(sys.argv)
    if Architecture.is_python_version(MINIMAL_PYTHON_VERSION_MAJOR, minor=MINIMAL_PYTHON_VERSION_MINOR):
        _start_app(app, args)
    else:
        _fail_app()
    app.exit()
    _close_app()



