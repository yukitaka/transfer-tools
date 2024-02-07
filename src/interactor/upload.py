import os
import json
from ..confluence.converter.title import joined_path
from ..confluence.model.pages import Pages as Confluence
from ..growi.model.pages import Pages as GrowiPages


class Growi:
    @staticmethod
    def attachments(args):
        for page in Confluence.filelist():
            attachments = page.attachments()
            if not attachments:
                continue
            for attachment in attachments:
                print(attachment.file())

    @staticmethod
    def is_page_uploaded(page):
        return os.path.exists(page.file_path() + '/growi.id')

    @staticmethod
    def pages(args):
        for page in Confluence.filelist():
            path = joined_path(page)

            if not Growi.is_page_uploaded(page):
                upload_path = os.environ.get('GROWI_PATH') + path

                res = GrowiPages.upload(upload_path, page.md())
                if not res:
                    continue
                print(res)
                growi_id = res['page']['_id']
                with open(page.file_path() + '/growi.id', 'w') as f:
                    f.write(growi_id)
                    print(f'Uploaded {path} to Growi')
                os.makedirs('data/growi/pages/' + growi_id, exist_ok=True)
                meta = {'path': res['page']['path'], 'updatedAt': res['page']['updatedAt']}
                with open('data/growi/pages/' + growi_id + '/meta.json', 'w') as f:
                    f.write(json.dumps(meta))
                with open('data/growi/pages/' + growi_id + '/confluence.id', 'w') as f:
                    f.write(page.id)
                with open('data/growi/pages/' + growi_id + '/page.md', 'w') as f:
                    f.write(page.md())
