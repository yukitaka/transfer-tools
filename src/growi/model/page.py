import os.path
from .attachment import Attachment
from ...utils.file import save_json

class Page:
    def __init__(self, gid):
        self.id = gid
        self.markdown = None

    def local_path(self):
        return f'data/growi/pages/{self.id}'

    def md(self):
        if self.markdown is not None:
            return self.markdown

        with open(f'{self.local_path()}/page.md') as f:
            self.markdown = f.read()

            return self.markdown

    def attachments(self):
        if not os.path.exists(f'{self.local_path()}/attachments'):
            return None
        for file in os.listdir(f'{self.local_path()}/attachments'):
            att = file.split('.')[0]
            yield Attachment(self.id, att)

    def add_attachment(self, att_id, attachment):
        path = f'{self.local_path()}/attachments'
        os.makedirs(path, exist_ok=True)
        save_json(f'{path}/{att_id}.json', attachment)
