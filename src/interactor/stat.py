from ..confluence.model.pages import Pages
from ..confluence.model.page import Page

class ConfluenceStat:
    @staticmethod
    def size(args):
        sizes = {}
        total = {}
        for page in Pages.filelist():
            if not page:
                continue

            parent = page.parent()
            if parent:
                sizes[page.id] = (parent.id, page.size())
            else:
                s = page.size()
                sizes[page.id] = (None, s)
                total[page.id] = s

        calc = list(total.keys())
        for k, v in sizes.items():
            pid = v[0]
            if not pid or k in calc:
                continue
            sz = 0
            kk = k
            vv = v
            while True:
                pkey = vv[0]
                sz += vv[1]
                if not pkey:
                    calc.append(kk)
                    break

                par = sizes[pkey]
                if kk in calc:
                    vv = par
                    kk = pkey
                    continue

                calc.append(kk)
                if pkey in total:
                    total[pkey] += sz
                    break
                pkey = vv[0]
                vv = sizes[pkey]
                kk = pkey


        for k, v in total.items():
            page = Page(k)
            title = page.json()['title']
            print(f'{title}({k}): {v}')