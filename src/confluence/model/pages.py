import glob
import os
from src.utils.logger import logger
from .base import Base
from .user import User
from .page import Page
from ..converter.to_md import Converter
from ...utils import store

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
            if not self.store_json(p):
                break

    def recently_convert(self, limit=50):
        files = glob.glob(f'{self.dir}/{self.mode}/*.json')
        files.sort(key=os.path.getmtime)
        for f in files[:limit]:
            path = f.replace('.json', '')
            page = store.load_json(f)
            author = User.get_user_by_id(page['version']['authorId'])
            date = page['createdAt']
            data = store.load_jsons(page['body']['atlas_doc_format']['value'])
            conv = f"Author: {author.name}\n"
            conv += f"Created: {date}\n\n"
            conv += Converter(data, path).md

            self.store(path + '.md', conv)

    def store_json(self, data):
        pid = data['id']
        path = self.dir + f'/{self.mode}/{pid}'
        logger.info(path)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        if self.store(path + '.json', data):
            return True
        logger.info(f'{data['version']['createdAt']} is older')

        return False

    def store(self, path, data):
        return Base.store(path, data)

    @staticmethod
    def recently(limit=50):
        lst = []
        for file in Pages.filelist():
            if len(lst) == 0:
                lst.append(file)
            else:
                created_at = file.json()['version']['createdAt']
                for k, v in enumerate(lst):
                    if created_at > v.json()['version']['createdAt']:
                        lst.insert(k, file)
                        break
                if len(lst) > limit:
                    lst = lst[:limit]

        return lst

    @staticmethod
    def filelist():
        for file in glob.iglob('data/confluence/pages/[0-9]*.json'):
            yield Page.from_file(file)
