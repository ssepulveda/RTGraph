import sys
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6 import uic

import functools
import asyncio
import qasync
from qasync import asyncSlot, asyncClose, QApplication

from enum import Enum


class States(Enum):
    Idle = 0
    Capturing = 1
    Error = -1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Variables
        self.state = States.Idle

        # load ui file
        uic.loadUi('rtgraph/ui/main.ui', self)

        # Signals
        self.resumeButton.clicked.connect(self.resume)

    @asyncClose
    async def closeEvent(self, event):
        print(f'Close stuff goes here: {event}')

    @asyncSlot()
    async def resume(self):
        if self.state == States.Idle:
            self.resumeButton.setText('Stop')
            print("Start adquiring data")
            self.state = States.Capturing
        elif self.state == States.Capturing:
            print("Closing stuff")
            await asyncio.sleep(1)
            self.resumeButton.setText('Start')
            self.state = States.Idle


async def main(argv):
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    app.aboutToQuit.connect(functools.partial(close_future, future, loop))

    mainWindow = MainWindow()
    mainWindow.show()

    await future
    return True


if __name__ == '__main__':
    try:
        qasync.run(main(sys.argv))
    except asyncio.exceptions.CancelledError:
        sys.exit(0)