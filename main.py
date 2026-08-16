
import sys
import asyncio
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication
from components.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
    sys.exit(app.exec())
