import glob
import time
import re
import os
from .base import Base
from src.utils import store
from src.utils.logger import logger

class Pages(Base):
    def __init__(self, path):
        self.path = 'data/growi' + path

    @staticmethod
    def get_confluence_id(file_name):
        m = re.match(r'[^\d]+(\d+).title$', file_name)
        if m is None:
            logger.fatal(f'Could not find {file_name}')

        return m.group(1)
    def recently_download(self, limit=10):
        files = glob.glob('data/confluence/pages/*.title')
        files.sort(key=os.path.getmtime)
        for f in files[:limit]:
            cid = self.get_confluence_id(f)
            if glob.glob(self.path + f'/*/{cid}.id'):
                continue
            with open(f, 'r') as f:
                path = f.read()
                data = Base.get('/page', {'path': path})
                if 'page' not in data:
                    print(cid, path)
                    continue
                pid = data['page']['_id']
                self.store(cid, pid, data)
            time.sleep(1)

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
