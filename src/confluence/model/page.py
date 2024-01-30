import re

class Page:
    def __init__(self, cid):
        self.id = cid

    def path(self):
        with open(f'data/confluence/pages/{self.id}.title', 'r') as f:
            return f.read()

    @staticmethod
    def from_file(file):
        m = re.match(r'[^\d]+(\d+).title$', file)
        if m:
            return Page(m.group(1))
