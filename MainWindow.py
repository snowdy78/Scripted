# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from SearchField import SearchField

class MainWindow(QWidget):
    it_topics = [
        "Python Programming",
        "PyQt6 Desktop Apps",
        "PySide6 Interfaces",
        "Qt Designer Layouts",
        "JavaScript Web Development",
        "TypeScript Applications",
        "React Frontend Framework",
        "Node.js Backend Server",
        "Data Science Analysis",
        "Machine Learning Models",
        "Deep Learning Networks",
        "Artificial Intelligence Systems",
        "SQL Database Management",
        "NoSQL Data Storage",
        "Git Version Control",
        "Docker Containerization",
        "Cloud Computing Services",
        "Linux System Administration",
        "Mobile App Development",
        "Cybersecurity Protocols"
    ]
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример с QLineEdit")
        self.resize(300, 150)

        # 1. Создаем вертикальный макет (Layout)
        layout = QVBoxLayout()

        # 2. Создаем поле ввода Line Edit
        self.search = SearchField(items = self.it_topics)
        layout.addWidget(self.search) # Добавляем в макет

        # 3. Создаем кнопку для считывания текста
        self.btn = QPushButton("Показать текст")
        self.btn.clicked.connect(self.print_text) # Привязываем функцию к клику
        layout.addWidget(self.btn) # Добавляем в макет

        # Устанавливаем макет для главного окна
        self.setLayout(layout)

    def print_text(self):
        # Метод .text() забирает строку из QLineEdit
        entered_text = self.search.text()
        print(f"Пользователь ввел: {entered_text}")

