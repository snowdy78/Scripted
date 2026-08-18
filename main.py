
import sys
import asyncio
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication
from Scripted.components.MainWindow import MainWindow
from Scripted.QssLoader import loadStyleSheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if style_sheet := loadStyleSheet("style/style.qss"):
        app.setStyleSheet(style_sheet)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
