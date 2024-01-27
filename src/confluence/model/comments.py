import glob
import os
from src.utils import store
from src.utils.logger import logger
from datetime import datetime, timezone
from .base import Base

class Comments(Base):
    def __init__(self, directory):
        super().__init__(directory)

    @staticmethod
    def list(limit=10):
        params = {"body-format": "atlas_doc_format", "limit": limit, "sort": "-modified-date"}

        return Base.get('/wiki/api/v2/footer-comments', params)

    def recently_download(self, limit=50):
        data = Comments.list(limit)
        for p in data['results']:
            if not self.store(p):
                break

    def store(self, data):
        pid = data['pageId']
        path = self.dir + f'/pages/{pid}/comments/'
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        search = False
        for filename in glob.glob(path + f'*-{data['id']}.json'):
            logger.info(filename)
            if not os.path.exists(filename):
                store.save_json(filename, data)

                return True

            mtime = datetime.fromtimestamp(os.stat(filename).st_mtime, tz=timezone.utc)
            if mtime < datetime.fromisoformat(data['version']['createdAt']):
                store.save_json(filename, data)

                return True
            search = True

        if not search:
            logger.error(path, data)

        return False
