from .model.pages import Pages

def pages(args):
    p = Pages('data/confluence', 'pages')
    p.recently_convert(int(args.recently))