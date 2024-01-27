import os
from datetime import datetime, timezone
from src.utils import store
from src.utils.logger import logger
from .base import Base

class Pages(Base):
    def __init__(self, directory, mode):
        super().__init__(directory)
        self.mode = mode

    @staticmethod
    def list(limit=10):
        params = {"body-format": "atlas_doc_format", "limit": limit, "sort": "-modified-date"}

        return Base.get('/wiki/api/v2/pages', params)


    def recently_download(self, limit=50):
        data = Pages.list(limit)
        for p in data['results']:
            if not self.store(p):
                break

    def store(self, data):
        pid = data['id']
        path = self.dir + f'/{self.mode}/{pid}'
        logger.info(path)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        if Base.store(path + '.json', data):
            return True

        logger.info(f'{data['version']['createdAt']} is older than {mtime}')

        return False
