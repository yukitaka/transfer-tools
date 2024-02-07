import os
from ..utils.file import save
from ..confluence.converter.title import joined_path
from ..confluence.model.pages import Pages as ConfluencePages
from ..confluence.model.comments import Comments as ConfluenceComments
from ..confluence.model.attachments import Attachments as ConfluenceAttachments

class Confluence:
    @staticmethod
    def pages(args):
        p = ConfluencePages('data/confluence', 'pages')
        p.recently_download(int(args.recently))
        for page in ConfluencePages.recently(int(args.recently)):
            growi_path = os.environ.get('GROWI_PATH') + joined_path(page)
            save(f'{page.file_path()}/title.txt', growi_path)

    @staticmethod
    def comments(args):
        c = ConfluenceComments('data/confluence')
        c.recently_download(int(args.recently))

    @staticmethod
    def attachments(args):
        a = ConfluenceAttachments('data/confluence')
        a.recently_download(int(args.recently))
