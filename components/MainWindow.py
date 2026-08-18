# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from components.panels.UploadKnowledgeBasePage import UploadKnowledgeBasePage
from config import initDatabase, closeDatabase
from components.panels.FindScriptPage import FindScriptPage
from components.panels.SettingsPage import SettingsPage
from components.panels.AskAiPage import AskAiPage
from components.PagesList import PagesList

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример с QLineEdit")
        self.resize(800, 600)
        initDatabase()
        # 1. Создаем вертикальный макет (Layout)
        main_layout = QHBoxLayout()
        # 2. Создаем список панелей

        panels = ["Обновление данных", "Ai", "Загрузка", "Настройки", "Выход"]
        # 3. Добавляем в макет список панелей
        self.panel_list = PagesList(panels)
        # pylint: disable=no-member
        self.panel_list.activated.connect(self.switchPanel)
        main_layout.addWidget(self.panel_list)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(FindScriptPage())
        self.stacked_widget.addWidget(AskAiPage())
        self.stacked_widget.addWidget(UploadKnowledgeBasePage())
        self.stacked_widget.addWidget(SettingsPage())
        main_layout.addWidget(self.stacked_widget)

        # 4. Устанавливаем макет для главного окна
        self.setLayout(main_layout)

    def switchPanel(self):
        index = self.panel_list.indexFromItem(self.panel_list.currentItem()).row()
        if index == self.panel_list.count() - 1:
            self.close()
        self.stacked_widget.setCurrentIndex(index)

    def closeEvent(self, event: QCloseEvent) -> None:
        closeDatabase()
        return super().closeEvent(event)
