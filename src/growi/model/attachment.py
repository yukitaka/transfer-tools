from ...utils.file import load_json

class Attachment:
    def __init__(self, gid, att):
        self.id = att
        self.page_id = gid
        self.json_blob = None

    def base_path(self):
        return f'data/growi/pages/{self.page_id}/attachments/{self.id}'

    def json(self):
        if not self.json_blob:
            self.json_blob = load_json(self.base_path() + '.json')
        return self.json_blob

    def file_name(self):
        return self.json()['originalName']
