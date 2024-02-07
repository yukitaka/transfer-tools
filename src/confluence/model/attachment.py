import os.path
from ...utils.file import load_json

class Attachment:
    def __init__(self, cid, att):
        self.id = att
        self.page_id = cid

    def base_path(self):
        return f'data/confluence/pages/{self.page_id}/attachments/{self.id}'

    def json(self):
        return load_json(self.base_path() + '.json')
    def file(self):
        name = self.json()['title']
        file_path = self.base_path().replace(self.id, name)
        if os.path.exists(file_path):
            return (name, open(file_path, 'rb'))
