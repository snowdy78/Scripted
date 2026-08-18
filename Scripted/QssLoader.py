import os

def loadStyleSheet(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        print(f"Предупреждение: Файл стилей {file_path} не найден.")
