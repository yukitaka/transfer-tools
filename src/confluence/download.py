from .model.attachments import Attachments

def attachments(args):
    p = Attachments('data/confluence')
    p.recently_download(args.recently)
