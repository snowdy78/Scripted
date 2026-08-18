import os
from PySide6.QtCore import QFile

def loadStyleSheet(file_path: str):
    if os.path.exists(file_path):
        style_file = QFile(file_path)
        style_file.setFileName(file_path)
        style_file.open(QFile.OpenModeFlag.ReadOnly)
        return style_file.readAll().toStdString()
    else:
        print(f"Предупреждение: Файл стилей {file_path} не найден.")
