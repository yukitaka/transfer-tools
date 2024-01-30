import glob
import time
import os
from .base import Base
from src.utils import store
from src.utils.logger import logger
from src.confluence.model.pages import Pages as Confluence

class Pages(Base):
    def __init__(self, path):
        self.path = 'data/growi' + path

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
        data = Base.get('/page', {'path': page.upload_path()})
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
            local_meta = store.load_json(json)
            if local_meta['updatedAt'] < meta['updatedAt']:
                should_store = True

        if should_store:
            logger.info(f'Storing page {pid}')
            store.save_file(base + '/' + cid + '.id', '')
            store.save_file(md, contents)
            store.save_json(json, meta)
