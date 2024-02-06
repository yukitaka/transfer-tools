import os
import json
from ..confluence.converter.title import joined_path
from ..confluence.model.pages import Pages as Confluence
from ..growi.model.pages import Pages as Growi

def is_uploaded(page):
    return os.path.exists(page.file_path() + '/growi.id')

def upload(args):
    for page in Confluence.filelist():
        path = joined_path(page)

        if not is_uploaded(page):
            upload_path = os.environ.get('GROWI_PATH') + path

            res = Growi.upload(upload_path, page.md())
            growi_id = res['data']['page']['_id']
            with open(page.file_path() + '/growi.id', 'w') as f:
                f.write(growi_id)
                print(f'Uploaded {path} to Growi')
            os.makedirs('data/growi/pages/' + growi_id, exist_ok=True)
            meta = {'path': res['data']['page']['path'], 'updatedAt': res['data']['page']['updatedAt']}
            with open('data/growi/pages/' + growi_id + '/meta.json', 'w') as f:
                f.write(json.dumps(meta))
            with open('data/growi/pages/' + growi_id + '/confluence.id', 'w') as f:
                f.write(page.id)
            with open('data/growi/pages/' + growi_id + '/page.md', 'w') as f:
                f.write(page.md())
