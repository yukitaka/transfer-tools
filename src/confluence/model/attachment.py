import os.path
from .base import Base
from ...utils.file import load_json
from ...utils.logger import logger

class Attachment:
    def __init__(self, cid, att):
        self.id = att
        self.page_id = cid
        self.json_blob = None

    def base_path(self):
        return f'data/confluence/pages/{self.page_id}/attachments/{self.id}'

    def json(self):
        if not self.json_blob:
            self.json_blob = load_json(self.base_path() + '.json')
        return self.json_blob

    def file_name(self):
        return self.json()['title']

    def file(self):
        name = self.file_name()
        file_path = self.base_path().replace(self.id, name)
        if os.path.exists(file_path):
            return name, open(file_path, 'rb'), self.json()['mediaType']

    def download(self):
        link = self.json()['downloadLink']
        file_name = self.json()['title']
        file_size = self.json()['fileSize']
        file_path = self.base_path().replace(self.id, file_name)
        if os.path.exists(file_path) and os.path.getsize(file_path) == file_size:
            logger.info(f'{file_name} already exists')
            return
        att = Base.get(f'/wiki{link}')
        if att.status_code == 404:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.remove(self.base_path() + '.json')
        else:
            with open(file_path, 'wb') as f:
                for chunk in att.iter_content(chunk_size=512):
                    f.write(chunk)
                f.flush()
                att.close()
                logger.info(f'{self.page_id}.{self.id} {file_name} downloaded')
