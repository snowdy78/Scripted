# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Qt, Signal, QStringListModel, QEvent
from PySide6.QtWidgets import QCompleter, QListView

class SearchCompleter(QCompleter):
    DEFAULT_MAX_VISIBLE_ITEMS = 8
    popup_hidden = Signal()
    def __init__(self, items, parent=None):
        super().__init__([], parent)

        self.popup_view = QListView()
        self.setPopup(self.popup_view)

        self.model = QStringListModel(items, self)
        self.setModel(self.model)

        self.setFilterMode(Qt.MatchFlag.MatchContains)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setMaxVisibleItems(self.DEFAULT_MAX_VISIBLE_ITEMS)
        self.popup().installEventFilter(self)

    def eventFilter(self, object, event):
        if object is self.popup():
            if event.type() == QEvent.Type.Show:
                print("Popup opens")
            if event.type() == QEvent.Type.Hide:
                print("popup hide")
                self.popup_hidden.emit()
        return super().eventFilter(object, event)

    def setCompletionPrefix(self, prefix):
        if prefix:
            super().setCompletionPrefix(prefix)
            return
        # Подмена: вместо "" передаем " ".
        # При MatchContains строка "Apple" содержит подстроку " ", поэтому фильтр сработает на ВСЕ элементы.
        super().setCompletionPrefix(" ")
        # Явно вызываем complete(), чтобы обновить список
        self.complete()

