class Attachment:
    def __init__(self, gid, att):
        self.id = att
        self.page_id = gid
        self.json_blob = None

    def base_path(self):
        return f'data/growi/pages/{self.page_id}/attachments/{self.id}'
