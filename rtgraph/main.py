import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton

import functools
import asyncio
import qasync
from qasync import asyncSlot, asyncClose, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('RTGraph')

        button = QPushButton('Press Me!')
        button.setCheckable(True)
        button.clicked.connect(self.test)

        # Set the central widget of the Window.
        self.setCentralWidget(button)

    @asyncClose
    async def closeEvent(self, event):
        print(f'Close stuff goes here: {event}')

    @asyncSlot()
    async def test(self):
        self.setEnabled(False)
        await asyncio.sleep(3)
        self.setEnabled(True)


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