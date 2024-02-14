import glob
import os.path
import re
from .user import User
from .attachment import Attachment
from ..converter.to_md import Converter
from .. import util_file
from ...utils.file import load_json

class Page:
    def __init__(self, cid):
        self.id = cid
        self.markdown = None

    def file_path(self):
        return f'data/confluence/pages/{self.id}'

    def json(self):
        return load_json(self.file_path() + '/page.json')

    def parent(self):
        pid = self.json()['parentId']
        if pid is None:
            return None

        return Page(int(self.json()['parentId']))

    def size(self):
        s = os.path.getsize(self.file_path() + '/page.json')
        for a in self.attachments():
            s += a.size()

        return s

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

    def attachments(self):
        for file in glob.iglob(f'data/confluence/pages/{self.id}/attachments/*.json'):
            att = file.split('/')[-1].split('.')[0]
            yield Attachment(self.id, att)

    @staticmethod
    def from_file(file):
        m = re.match(r'[^\d]+(\d+)/page.json$', file)
        if m:
            return Page(int(m.group(1)))
