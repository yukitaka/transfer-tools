import glob
import time
import os
from .base import Base
from .page import Page
from src.utils import file
from src.utils.logger import logger
from src.confluence.model.pages import Pages as Confluence


class Pages(Base):
    def __init__(self, path):
        self.path = 'data/growi' + path

    @staticmethod
    def get(path):
        return Base.get_request('/page', {'path': path})

    @staticmethod
    def upload(path, data):
        current = Pages.get(path)
        if type(current) == int and current == 404:
            return Base.post_request('/pages', json={'path': path, 'body': data })
        else:
            print('Before ------------------')
            print(current)
            print('After ------------------')
            print(data)

    def upload_all(self):
        pass

    def download_all(self):
        for page in Confluence.filelist():
            if not page:
                continue
            if not page.is_uploaded():
                continue
            if self.download(page):
                time.sleep(1)

    def download(self, page):
        if glob.glob(self.path + f'/*/{page.id}.id'):
            return False
        data = Base.get_request('/page', {'path': page.upload_path()})
        if 'page' not in data:
            return False
        pid = data['page']['_id']
        self.store(page.id, pid, data)

        return True

    def store(self, cid, pid, data):
        meta = {'updatedAt': data['page']['updatedAt'], 'path': data['page']['path']}
        contents = data['page']['revision']['body']
        base = self.path + '/' + pid
        json = base + '/meta.json'
        md = base + '/page.md'
        should_store = False

        os.makedirs(base, exist_ok=True)
        if not os.path.exists(md):
            should_store = True
        else:
            local_meta = file.load_json(json)
            if local_meta['updatedAt'] < meta['updatedAt']:
                should_store = True

        if should_store:
            logger.info(f'Storing page {pid}')
            file.save(base + '/' + cid + '.id', '')
            file.save(md, contents)
            file.save_json(json, meta)
    @staticmethod
    def filelist():
        for directory in glob.iglob('data/growi/pages/*'):
            yield Page(directory.split('/')[-1])
