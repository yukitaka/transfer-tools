from .model.comments import Comments
from .model.attachments import Attachments

def comments(args):
    p = Comments('data/confluence')
    p.recently_download(args.recently)

def attachments(args):
    p = Attachments('data/confluence')
    p.recently_download(args.recently)
