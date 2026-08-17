from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from qasync import asyncSlot
from ParseTypes import ParseRequestData, ParseParams
from ScriptParser import findScriptOrParse
from components.Dropdown import Dropdown
from components.LoadingWidget import LoadingWidget

class FindScriptPanel(QWidget):
    topics = {
        "Мобильная карта": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/mobilnaja-karta-1/'),
        "Агророс Банк": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/agroros-bank/'),
        "Термекс": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/termeks/'),
        "Азбука Вкуса": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/azbuka-vkusa/'),
        "Благо": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/blago/'),
        "Мой Оператор": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/mojj-operator/'),
        "Газпром ГМТ": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/gazprom-gmt/'),
        "Внутренняя ГЛ": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/vnutrennjaja-gl/'),
        "Пицца Ханс": ParseParams('https://wiki.yandex.ru/homepage/1d169aa832c9/proekty-ogl/picca-xans/picca-xans-skript/')
    }
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        # 2. Создаем поле ввода Line Edit
        self.dropdown = Dropdown(items = list(self.topics.keys()))
        main_layout.addWidget(self.dropdown) # Добавляем в макет

        self.alert_label = QLabel()
        self.alert_label.setStyleSheet("color: #e00;")
        main_layout.addWidget(self.alert_label)
        self.button = QPushButton("Parse")
        # 3. Создаем кнопку для считывания текста
        # pylint: disable=no-member
        self.button.clicked.connect(self.print_text) # Привязываем функцию к клику
        main_layout.addWidget(self.button) # Добавляем в макет

        self.loading_widget = LoadingWidget()
        self.loading_widget.hide()
        sp = self.loading_widget.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.loading_widget.setSizePolicy(sp)
        main_layout.addWidget(self.loading_widget)
        main_layout.setContentsMargins(50, 50, 50, 50)
        # Устанавливаем макет для главного окна
        self.setLayout(main_layout)

    @asyncSlot()
    async def print_text(self):
        # Метод .text() забирает строку из QLineEdit
        line_edit = self.dropdown.lineEdit()
        if line_edit is None:
            return
        entered_text = line_edit.text().strip()
        parse_data = self.topics.get(entered_text)
        if parse_data is None:
            self.alert_label.setText("Тематика не найдена. Невозможно парсить.")
            return
        self.loading_widget.show()
        try:
            await findScriptOrParse(entered_text, None, ParseRequestData(parse_data))
        except Exception as e:
            self.alert_label.setText("Ошибка попробуйте еще раз.")
            print(e)
        finally:
            self.loading_widget.hide()
