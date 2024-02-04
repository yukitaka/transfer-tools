import os.path


class Page:
    def __init__(self, gid):
        self.id = gid
        self.markdown = None

    def local_path(self):
        return f'data/growi/pages/{self.id}'

    def md(self):
        if self.markdown is not None:
            return self.markdown

        with open(f'{self.local_path()}/page.md') as f:
            self.markdown = f.read()

            return self.markdown
