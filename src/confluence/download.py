import os
from .model.pages import Pages
from .model.comments import Comments

def pages(args):
    p = Pages('data', 'pages')
    p.recently_download(args.recently)

def comments(args):
    p = Comments('data')
    p.recently_download(args.recently)
