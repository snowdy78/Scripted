from PySide6.QtWidgets import QListWidget, QVBoxLayout

class PagesList(QListWidget):
    def __init__(self, panels, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setFixedWidth(200)
        self.setLayout(layout)
        self.addItems(panels)
        self.setStyleSheet("""
            QListWidget::item {
                text-align: center;
            }
        """)
