
from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import Qt, Signal, QStringListModel

class SearchCompleter(QCompleter):
    DEFAULT_MAX_VISIBLE_ITEMS = 4
    hidden = Signal()
    def __init__(self, items, parent=None):
        super().__init__([], parent)
        self.setModel(QStringListModel(items, self))
        self.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setMaxVisibleItems(self.DEFAULT_MAX_VISIBLE_ITEMS)
