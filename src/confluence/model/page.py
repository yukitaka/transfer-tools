import os.path
import re
from src.utils.store import load_json

class Page:
    def __init__(self, cid):
        self.id = cid

    def file_path(self):
        return f'data/confluence/pages/{self.id}'

    def json(self):
        return load_json(self.file_path() + '.json')

    def is_uploaded(self):
        return os.path.exists(self.file_path() + '.title')

    def upload_path(self):
        with open(self.file_path() + '.title', 'r') as f:
            return f.read()

    @staticmethod
    def from_file(file):
        m = re.match(r'[^\d]+(\d+).json$', file)
        if m:
            return Page(m.group(1))
