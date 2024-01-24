import os
from .model.pages import Pages

def pages(args):
    print(args)
    p = Pages('data', 'pages')
    p.recently_download(args.recently)
    print(os.environ['CONFLUENCE_DOMAIN'])
    print(os.environ['ATLASSIAN_USER'])
    print(os.environ['ATLASSIAN_TOKEN'])
