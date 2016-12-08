import multiprocessing
from PyQt4 import QtGui

from ui import mainWindow
from commons.logger import *
from commons.argParser import *


if __name__ == '__main__':
    multiprocessing.freeze_support()
    args = ArgParser()
    args.create()
    args.parse()
    user_info()

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
