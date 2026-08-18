import os
import json
from Config import Config

class Settings(Config):
    DEFAULT_SETTINGS = {
        "settings": {
            "theme": "Системная",
            "database": {
                "host": "localhost",
                "port": 0,
                "user": "root",
                "password": "",
                "database": "scripted"
            }
        }
    }
    SETTINGS_FILE = "settings.json"
    DUMP_INDENT = 2
    DUMP_ENSURE_ASCII = False

    def __init__(self):
        pass

    @staticmethod
    def filepath():
        return os.path.join(Config.CONFIG_DIR, Settings.SETTINGS_FILE)

    @staticmethod
    def get():
        Settings._initIfNotExists(Settings.SETTINGS_FILE, Settings.reset)
        with open(Settings.filepath(), "r", encoding="utf-8") as f:
            return json.load(f)
        raise FileNotFoundError("'settings.json' not found")

    @staticmethod
    def save(settings):
        with open(Settings.filepath(), "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=Settings.DUMP_INDENT, ensure_ascii=Settings.DUMP_ENSURE_ASCII)

    @staticmethod
    def reset():
        with open(Settings.filepath(), "w", encoding="utf-8") as f:
            json.dump(Settings.DEFAULT_SETTINGS, f, indent=Settings.DUMP_INDENT, ensure_ascii=Settings.DUMP_ENSURE_ASCII)
