import glob
import os
from src.utils import store

from .base import Base

class Pages(Base):
    def recently_download(self, limit=10):
        files = glob.glob('data/confluence/pages/*.title')
        files.sort(key=os.path.getmtime)
        for f in files[:limit]:
            with open(f, 'r') as f:
                path = f.read()
                data = Base.get('/page', {'path': path})
                pid = data['page']['_id']
                print(pid)
                print(data['page']['revision']['body'])