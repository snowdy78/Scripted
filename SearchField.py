# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal
from SearchCompleter import SearchCompleter

class SearchField(QLineEdit):
    focused = Signal()
    def __init__(self, items: list[str] = [], placeholder: str = "Введите текст здесь..."):
        super().__init__()
        self.items = items
        self.setPlaceholderText(placeholder) # Текст-подсказка

        self.completer = SearchCompleter(self.items)
        self.setCompleter(self.completer)

        self.choosed = self.completer.activated
        self.completer.activated.connect(self.itemChoosedEvent)
        self.completer.popup_hidden.connect(self.clearFocus)
        self.textChanged.connect(self.onTextChanged)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.completer.setCompletionPrefix(self.text() if self.text() else " ")
        self.focused.emit()
        self.completer.complete()
        print("focusing: ", self.hasFocus(), "enabled: ", self.isEnabled(), "readonly: ", self.isReadOnly())

    def onTextChanged(self, text):
        print(f"'{text}'")
        self.completer.setCompletionPrefix(text)
        self.completer.complete()

    def itemChoosedEvent(self, item):
        self.choose_callback(item)

