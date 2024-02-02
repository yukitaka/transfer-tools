import os
from ..utils.store import save_file
from ..confluence.converter.title import joined_path
from ..confluence.model.pages import Pages as ConfluencePages
from ..confluence.model.comments import Comments as ConfluenceComments

class Confluence:
    @staticmethod
    def pages(args):
        p = ConfluencePages('data/confluence', 'pages')
        p.recently_download(int(args.recently))
        for page in ConfluencePages.recently(int(args.recently)):
            growi_path = os.environ.get('GROWI_PATH') + joined_path(page)
            save_file(f'{page.file_path()}/title.txt', growi_path)

    @staticmethod
    def comments(args):
        c = ConfluenceComments('data/confluence')
        c.recently_download(int(args.recently))
