import json
import os


class Config():

    FILE = {}
    DEFAULT = {}
    ENV = {}

    def __init__(self, conf_file_path: str) -> None:
        self.FILE = conf_file_path
        if os.path.exists(conf_file_path):
            self.load(conf_file_path)

    def load(self, file_path: str) -> dict:
        if not file_path:
            return {}
        elif file_path != self.FILE:
            self.FILE = file_path
        with open(file_path, 'r') as fl:
            converted = json.load(fl)
            self.DEFAULT = converted['DEFAULT']
            self.ENV = converted['ENV']
        return converted

