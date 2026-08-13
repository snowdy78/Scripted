# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QComboBox
from SearchCompleter import SearchCompleter

class Dropdown(QComboBox):
    def __init__(self, items: list[str] = [], placeholder: str = "Введите текст здесь..."):
        super().__init__()
        self.items = items
        self.setPlaceholderText(placeholder) # Текст-подсказка
        self.setEditable(True)
        completer = SearchCompleter(self.items)
        self.setCompleter(completer)
        if items:
            self.addItems(items)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.showPopup()

    def onTextChanged(self, text):
        pass
