class Attachment:
    def __init__(self, gid, att):
        self.id = att
        self.page_id = gid
        self.json_blob = None
