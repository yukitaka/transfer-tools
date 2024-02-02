import os

from ..confluence.converter.title import joined_path
from ..confluence.model.pages import Pages as Confluence

def upload(args):
    for page in Confluence.filelist():
        path = joined_path(page)

        if page.is_uploaded():
            new = os.environ.get('GROWI_PATH') + path
            if new != page.upload_path():
                print(page.id)
                print('   ' + path)
                print(page.upload_path())
