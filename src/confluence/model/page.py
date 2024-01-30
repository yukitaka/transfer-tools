import os.path
import re

class Page:
    def __init__(self, cid):
        self.id = cid

    def path(self):
        return f'data/confluence/pages/{self.id}'

    def is_uploaded(self):
        return os.path.exists(self.path() + '.title')

    def upload_path(self):
        with open(self.path() + '.title', 'r') as f:
            return f.read()

    @staticmethod
    def from_file(file):
        m = re.match(r'[^\d]+(\d+).json$', file)
        if m:
            return Page(m.group(1))
