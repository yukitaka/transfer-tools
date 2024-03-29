import sys
import glob
from difflib import context_diff
from ..growi.model.pages import Pages as GrowiPages
from ..confluence.model.page import Page as ConfluencePage

class Diff:
    def pages(self):
        for page in GrowiPages.filelist():
            growi = page.md().split('\n')
            cid = Diff.confluence_id(page)
            cpage = ConfluencePage(cid)
            confluence = cpage.md().split('\n')
            diff = list(context_diff(growi, confluence, fromfile=page.id, tofile=cpage.id))
            if len(diff) > 0:
                for line in diff:
                    print(line, end='')
                print("\n")

    @staticmethod
    def confluence_id(page):
        path = page.local_path() + '/*.id'
        paths = glob.glob(path)
        if paths:
            return paths[0].split('/')[-1].split('.')[0]
