import json
import os


class Config():

    FILE = {}
    DEFAULT = {}
    METADATA = {}

    def __init__(self, conf_file_path: str) -> None:
        self.FILE = conf_file_path
        if os.path.exists(conf_file_path):
            self.load(conf_file_path)

    def load(self, file_path: str) -> dict:
        if not file_path:
            return {}
        with open(file_path, 'r') as fl:
            converted = json.load(fl)
            self.DEFAULT = converted['DEFAULT']
            self.METADATA = converted['METADATA']
        return converted

