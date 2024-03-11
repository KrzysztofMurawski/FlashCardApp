import configparser
from src.helpers import config_file_path


class ConfigProvider:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_window_width(self):
        return int(self.config["gui"]["window_width"])

    def get_window_height(self):
        return int(self.config["gui"]["window_height"])


config = ConfigProvider(config_file_path)
