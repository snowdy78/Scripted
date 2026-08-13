# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QComboBox, QCompleter
from PySide6.QtCore import Qt, QEvent, QStringListModel

class Dropdown(QComboBox):
    DEFAULT_MAX_VISIBLE_ITEMS = 8
    def __init__(
        self,
        items: list[str] = [],
        placeholder: str = "Введите текст здесь..."
    ):
        super().__init__()
        self.items = items
        self.setEditable(True)
        self._completer = QCompleter(self.items)

        self.setModel(QStringListModel(items, self))
        self._completer.setCompletionMode(
            QCompleter.CompletionMode.UnfilteredPopupCompletion
        )
        self._completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._completer.setMaxVisibleItems(self.DEFAULT_MAX_VISIBLE_ITEMS)
        self.setCompleter(self._completer)
        self.setPlaceholderText(placeholder) # Текст-подсказка
        if self.items:
            self.addItems(self.items)
        self.lineEdit().installEventFilter(self)

    def eventFilter(self, watched, event):
        # Если кликнули мышкой по текстовому полю ввода
        if watched == self.lineEdit() and event.type() == QEvent.Type.MouseButtonPress:
            # Проверяем, назначен ли комплитер
            if self._completer:
                # Вызываем именно popup от completer
                self._completer.complete()
                return True  # Событие обработано
        return super().eventFilter(watched, event)
