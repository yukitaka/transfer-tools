import json
import os.path
import re
from src.utils.file import load_json
from .user import User
from ..converter.to_md import Converter
from .. import util_file

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

        path = self.file_path() + '/page.md'
        if os.path.exists(path):
            with open(self.file_path() + '/page.md') as f:
                self.markdown = f.read()

                return self.markdown
        else:
            page = self.json()
            author = User.get_user_by_id(page['version']['authorId'])
            date = page['createdAt']
            data = load_json(page['body']['atlas_doc_format']['value'])
            conv = f"Author: {author.name}\n"
            conv += f"Created: {date}\n\n"
            conv += Converter(data, self.file_path()).md

            util_file.save(self.file_path() + '/page.md', conv)

            return conv

    @staticmethod
    def from_file(file):
        m = re.match(r'[^\d]+(\d+)/page.json$', file)
        if m:
            return Page(m.group(1))
