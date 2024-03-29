import re
from ..model.page import Page

def joined_path(page):
    tree = []
    current_page = page
    while True:
        json = current_page.json()
        if not json:
            break
        parent_id = json['parentId']
        if not parent_id:
            break
        title = json['title']
        title = title.replace('/', '-').replace(':', '：').replace('+', '＋').replace('?', '？')
        title = title.replace('　', ' ').strip()
        tree.append(title)
        current_page = Page(parent_id)

    tree.reverse()
    root = re.sub(r'pages.*', '', page.json()['_links']['webui'].replace('/overview', ''))

    return root + '/'.join(tree)
