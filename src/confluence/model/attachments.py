import os
import glob
from .base import Base
from .attachment import Attachment
from .page import Page
from .. import util_file

class Attachments(Base):
    def __init__(self, directory):
        super().__init__(directory)

    @staticmethod
    def list(limit=10):
        params = {"limit": limit, "sort": "-modified-date"}

        return Base.get('/wiki/api/v2/attachments', params)

    def downloads(self, limit=50):
        data = Attachments.list(limit)
        for p in data['results']:
            if not self.store(p):
                break

    def store(self, data):
        pid = data['pageId']
        version = data['version']['number']
        if version > 1:
            page = Page(pid)
            for att in page.attachments():
                json = att.json()
                if json['title'] == data['title'] and json['version']['number'] >= version:
                    os.remove(att.base_path() + '.json')

        path = self.dir + f'/pages/{pid}/attachments/'
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        filename = path + data['id'] + '.json'
        util_file.save(filename, data)

    @staticmethod
    def filelist():
        for file in glob.iglob('data/confluence/pages/[0-9]*/attachments/*.json'):
            page_id = file.split('/')[-3]
            att_id = file.split('/')[-1].split('.')[0]
            yield Attachment(page_id, att_id)
