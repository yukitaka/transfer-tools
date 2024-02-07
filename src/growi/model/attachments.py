from .base import Base

class Attachments(Base):
    @staticmethod
    def upload(id, attachment):
        return Base.post_request('/attachments.add', data={'page_id': id}, files={'file': attachment}, v=2)
