from .model.pages import Pages
def pages(args):
    p = Pages('/pages')
    if args.all:
        p.download_all()
