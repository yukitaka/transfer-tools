import os.path
from ...utils.file import load_json

class Attachment:
    def __init__(self, cid, att):
        self.id = att
        self.page_id = cid

    def file_path(self):
        return f'data/confluence/pages/{self.page_id}/attachments/{self.id}'

    def json(self):
        print(self.file_path())
        return load_json(self.file_path())
    def file(self):
        name = self.json()['title']
        file_path = self.file_path().replace(self.id, name)
        if os.path.exists(file_path):
            return {'file': (name, open(file_path, 'rb'))}
