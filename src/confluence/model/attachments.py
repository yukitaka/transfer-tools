import os
from .base import Base
from .. import util_file

class Attachments(Base):
    def __init__(self, directory):
        super().__init__(directory)

    @staticmethod
    def list(limit=10):
        params = {"limit": limit, "sort": "-modified-date"}

        return Base.get('/wiki/api/v2/attachments', params)

    def recently_download(self, limit=50):
        data = Attachments.list(limit)
        for p in data['results']:
            if not self.store(p):
                break

    def store(self, data):
        pid = data['pageId']
        path = self.dir + f'/pages/{pid}/attachments/'
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        filename = path + data['id'] + '.json'
        util_file.save(filename, data)
