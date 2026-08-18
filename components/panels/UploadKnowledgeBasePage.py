from PySide6.QtWidgets import QWidget, QVBoxLayout

class UploadKnowledgeBasePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
