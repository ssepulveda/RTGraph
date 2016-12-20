import sys
import multiprocessing
from PyQt4 import QtGui

from ui import mainWindow
from common.arguments import *
from common.architecture import Architecture
from common.logger import Logger as Log

MINIMAL_PYTHON_VERSION_MAJOR = 3
MINIMAL_PYTHON_VERSION_MINOR = 2


TAG = "RTGraph"


def _init_logger():
    args = Arguments()
    args.create()
    args.set_user_log_level()
    return args


def _start_app(app, args):
    Log.i(TAG, "Starting RTGraph")
    win = mainWindow.MainWindow(samples=args.get_user_samples())
    win.show()
    app.exec()

    Log.i(TAG, "Finishing RTGraph\n")
    win.close()


def _fail_app():
    txt = str("RTGraph requires Python {}.{} to run"
              .format(MINIMAL_PYTHON_VERSION_MAJOR, MINIMAL_PYTHON_VERSION_MINOR))
    Log.e(TAG, txt)


def _close_app():
    Log.close()
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



