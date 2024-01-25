import os
from .model.pages import Pages

def pages(args):
    p = Pages('data', 'pages')
    p.recently_download(args.recently)
