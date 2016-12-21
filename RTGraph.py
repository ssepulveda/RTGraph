import multiprocessing
import sys
from PyQt4 import QtGui

from rtgraph.common.architecture import Architecture
from rtgraph.common.arguments import *
from rtgraph.common.logger import Logger as Log
from rtgraph.core.constants import MinimalPython
from rtgraph.ui import mainWindow


TAG = "RTGraph"


class RTGraph:
    def __init__(self, argv=sys.argv):
        self.args = self._init_logger()
        self.app = QtGui.QApplication(argv)

    def start(self):
        if Architecture.is_python_version(MinimalPython.major, minor=MinimalPython.minor):
            Log.i(TAG, "Starting RTGraph")
            win = mainWindow.MainWindow(samples=self.args.get_user_samples())
            win.setWindowTitle("{} - {}".format(Constants.app_title, Constants.app_version))
            win.show()
            self.app.exec()

            Log.i(TAG, "Finishing RTGraph\n")
            win.close()
        else:
            self._fail()

    def close(self):
        self.app.exit()
        Log.close()
        sys.exit()

    @staticmethod
    def _init_logger():
        args = Arguments()
        args.create()
        args.set_user_log_level()
        return args

    @staticmethod
    def _fail():
        txt = str("RTGraph requires Python {}.{} to run"
                  .format(MinimalPython.major, MinimalPython.minor))
        Log.e(TAG, txt)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = RTGraph()
    app.start()
    app.close()



