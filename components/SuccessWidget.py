from PySide6.QtWidgets import QWidget
from PySide6.QtSvg import QSvgRenderer

class SuccessWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.renderer = QSvgRenderer("icons/success.svg")
        self.setFixedSize(self.renderer.defaultSize())
