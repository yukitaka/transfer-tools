from .base import Base

class Attachments(Base):
    @staticmethod
    def get(attachment_id):
        return Base.get_request(f'/attachment/{attachment_id}')

    @staticmethod
    def upload(page_id, attachment):
        return Base.post_request('/attachments.add', data={'page_id': page_id}, files={'file': attachment}, v=2)
