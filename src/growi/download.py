from .model.pages import Pages
def pages(args):
    p = Pages('/pages')
    p.recently_download(int(args.recently))
