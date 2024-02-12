from .base import Base

class Attachments(Base):
    @staticmethod
    def list(page_id):
        return Base.get_request(f'/attachment/list', query={'pageId': page_id})

    @staticmethod
    def get(attachment_id):
        return Base.get_request(f'/attachment/{attachment_id}')

    @staticmethod
    def upload(page_id, attachment):
        return Base.post_request('/attachments.add', data={'page_id': page_id}, files={'file': attachment}, v=2)

    @staticmethod
    def remove(attachment_id):
        return Base.post_request('/attachments.remove', data={'attachment_id': attachment_id}, v=2)
