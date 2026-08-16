
import sys
from PySide6.QtWidgets import QApplication
from components.MainWindow import MainWindow
from config import database

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    database.close()
    sys.exit(app.exec())
