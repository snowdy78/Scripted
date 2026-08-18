from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout
from PySide6.QtCore import Qt
from qasync import asyncSlot
from Settings import Settings

class SettingsPage(QWidget):
    THEME_VALUES = ["Темная", "Светлая", "Системная"]
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(QLabel("Тема"), 0, 0)
        self.themes = QComboBox()
        self.themes.addItems(self.THEME_VALUES)

        self.host_field = QLineEdit("")
        self.port_field = QLineEdit("")
        self.user_field = QLineEdit("")
        self.password_field = QLineEdit("")
        self.dbname_field = QLineEdit("")

        self.reset_btn = QPushButton("Сброс")
        self.save_btn = QPushButton("Сохранить")
        # pylint: disable=no-member
        self.reset_btn.clicked.connect(self.resetSettings)
        self.save_btn.clicked.connect(self.saveSettings)
        self.updateFields()

        layout.addWidget(self.themes, 0, 1)
        # TODO bd header
        layout.addWidget(QLabel("Хост БД"), 1, 0)
        layout.addWidget(self.host_field, 1, 1)

        layout.addWidget(QLabel("Порт БД"), 2, 0)
        layout.addWidget(self.port_field, 2, 1)

        layout.addWidget(QLabel("Пользователь БД"), 3, 0)
        layout.addWidget(self.user_field, 3, 1)

        layout.addWidget(QLabel("Пароль БД"), 4, 0)
        layout.addWidget(self.password_field, 4, 1)

        layout.addWidget(QLabel("Название БД"), 5, 0)
        layout.addWidget(self.dbname_field, 5, 1)


        layout.addWidget(self.reset_btn, 6, 0)
        layout.addWidget(self.save_btn, 6, 1)

        self.setLayout(layout)

    def updateFields(self):
        self.settings_json = Settings.get()
        self.settings = self.settings_json["settings"]
        self.theme_setting = self.settings["theme"]
        self.db_setting = self.settings["database"]

        self.themes.setCurrentIndex(self.THEME_VALUES.index(self.theme_setting))
        self.host_field.setText(self.db_setting["host"])
        self.port_field.setText(str(self.db_setting["port"]))
        self.user_field.setText(self.db_setting["user"])
        self.password_field.setText(self.db_setting["password"])
        self.dbname_field.setText(self.db_setting["database"])

    @asyncSlot()
    async def resetSettings(self):
        Settings.reset()
        self.updateFields()

    @asyncSlot()
    async def saveSettings(self):
        json_data = {
            "settings": {
                "theme": self.themes.currentText(),
                "database": {
                    "host": self.host_field.text(),
                    "port": int(self.port_field.text()),
                    "user": self.user_field.text(),
                    "password": self.password_field.text(),
                    "database": self.dbname_field.text()
                }
            }
        }
        Settings.save(json_data)
        self.updateFields()
