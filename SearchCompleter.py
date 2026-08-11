# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Qt, Signal, QStringListModel, QEvent
from PySide6.QtWidgets import QCompleter, QListView, QLineEdit
from typing import cast

class SearchCompleter(QCompleter):
    DEFAULT_MAX_VISIBLE_ITEMS = 4
    hidden = Signal()
    def __init__(self, items, parent=None):
        super().__init__([], parent)
        self.setModel(QStringListModel(items, self))
        self.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setMaxVisibleItems(self.DEFAULT_MAX_VISIBLE_ITEMS)

    def setCompletionPrefix(self, prefix = ""):
        super().setCompletionPrefix(prefix if prefix else " ")

