from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel

class AskAiPage(QWidget):
    class AiAnswerLabel(QLabel):
        pass

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.answer_label = AskAiPage.AiAnswerLabel("text")
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Спроси ИИ!")
        # pylint: disable=no-member
        self.line_edit.returnPressed.connect(self.ask)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.answer_label)
        layout.addStretch(1)
        self.setLayout(layout)

    def ask(self, question: str) -> None:
        """Get the answer from the AI"""
        question = self.line_edit.text()
        self.answer_label.setText(self.answer(question))

    def answer(self, question: str) -> str:
        return "some answer"
