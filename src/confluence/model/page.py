import os.path
import re
from src.utils.store import load_json

class Page:
    def __init__(self, cid):
        self.id = cid
        self.markdown = None

    def file_path(self):
        return f'data/confluence/pages/{self.id}'

    def json(self):
        return load_json(self.file_path() + '/page.json')

    def md(self):
        if self.markdown is not None:
            return self.markdown

        with open(self.file_path() + '/page.md') as f:
            self.markdown = f.read()

            return self.markdown

    def is_uploaded(self):
        return os.path.exists(self.file_path() + '/title.txt')

    def upload_path(self):
        with open(self.file_path() + '/title.txt', 'r') as f:
            return f.read()

    @staticmethod
    def from_file(file):
        m = re.match(r'[^\d]+(\d+)/page.json$', file)
        if m:
            return Page(m.group(1))
