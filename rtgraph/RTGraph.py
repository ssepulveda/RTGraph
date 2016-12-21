import multiprocessing
import sys

from PyQt4 import QtGui
from rtgraph.common.architecture import Architecture
from rtgraph.common.arguments import *
from rtgraph.common.logger import Logger as Log
from rtgraph.core.constants import MinimalPython

from rtgraph.ui import mainWindow


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
              .format(MinimalPython.major, MinimalPython.minor))
    Log.e(TAG, txt)


def _close_app():
    Log.close()
    sys.exit()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    args = _init_logger()

    app = QtGui.QApplication(sys.argv)
    if Architecture.is_python_version(MinimalPython.major, minor=MinimalPython.minor):
        _start_app(app, args)
    else:
        _fail_app()
    app.exit()
    _close_app()



