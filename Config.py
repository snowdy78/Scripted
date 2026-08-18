import os

class Config:
    CONFIG_DIR = "config"
    def __init__(self):
        pass

    @staticmethod
    def _initIfNotExists(file_name, reset_func):
        if not os.path.exists(Config.CONFIG_DIR):
            os.mkdir(Config.CONFIG_DIR)
        if not os.path.isfile(os.path.join(Config.CONFIG_DIR, file_name)):
            reset_func()
