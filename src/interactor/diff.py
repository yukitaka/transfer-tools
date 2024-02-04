from ..growi.model.pages import Pages as GrowiPages

class Diff:
    def pages(self):
        for page in GrowiPages.filelist():
            print(page)
