from .model.pages import Pages
def pages(args):
    p = Pages()
    p.recently_download(int(args.recently))
