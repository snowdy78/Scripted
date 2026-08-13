# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from Dropdown import Dropdown
from ParseTypes import ParseParams

class MainWindow(QWidget):
    it_topics = {
        "Мобильная карта": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/mobilnaja-karta-1/'),
        "Агророс Банк": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/agroros-bank/'),
        "Термекс": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/termeks/'),
        "Азбука Вкуса": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/azbuka-vkusa/'),
        "Благо": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/blago/'),
        "Мой Оператор": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/mojj-operator/'),
        "Газпром ГМТ": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/gazprom-gmt/'),
        "Внутренняя ГЛ": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/vnutrennjaja-gl/')
    }
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример с QLineEdit")
        self.resize(800, 600)

        # 1. Создаем вертикальный макет (Layout)
        layout = QVBoxLayout()

        # 2. Создаем поле ввода Line Edit
        self.dropdown = Dropdown(items = list(self.it_topics.keys()))
        layout.addWidget(self.dropdown) # Добавляем в макет

        # 3. Создаем кнопку для считывания текста
        self.btn = QPushButton("Показать текст")
        self.btn.clicked.connect(self.print_text) # Привязываем функцию к клику
        layout.addWidget(self.btn) # Добавляем в макет

        # Устанавливаем макет для главного окна
        self.setLayout(layout)

    def print_text(self):
        # Метод .text() забирает строку из QLineEdit
        entered_text = self.dropdown.currentData()
        print(f"Пользователь ввел: {entered_text}")

