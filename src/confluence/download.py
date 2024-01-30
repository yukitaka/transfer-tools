from .model.pages import Pages
from .model.comments import Comments
from .model.attachments import Attachments

def pages(args):
    p = Pages('data/confluence', 'pages')
    p.recently_download(args.recently)

def comments(args):
    p = Comments('data/confluence')
    p.recently_download(args.recently)

def attachments(args):
    p = Attachments('data/confluence')
    p.recently_download(args.recently)
