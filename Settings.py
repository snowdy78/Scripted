import json
import os
import sys

class Settings:
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
    SETTINGS_PATH = "config/settings.json"
    def __init__(self):
        pass

    @staticmethod
    def get():
        # TODO check if dir not exist
        with open(Settings.SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
        raise FileNotFoundError("'settings.json' not found")

    @staticmethod
    def save(settings):
        with open(Settings.SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)

    @staticmethod
    def reset():
        with open(Settings.SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(Settings.DEFAULT_SETTINGS, f, indent=4, ensure_ascii=False)
