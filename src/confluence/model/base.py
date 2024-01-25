import json
import os
import requests
from requests.auth import HTTPBasicAuth
from src.utils.logger import logger

class Base:
    def __init__(self, directory):
        self.dir = directory

    @staticmethod
    def get(path, query=None):
        return Base.request('get', path, query)

    @staticmethod
    def post(path, query=None):
        return Base.request('post', path, query)

    @staticmethod
    def request(method, path, query=None):
        domain = os.environ['CONFLUENCE_DOMAIN']
        user = os.environ['ATLASSIAN_USER']
        token = os.environ['ATLASSIAN_TOKEN']
        if query is None:
            query = {}

        url = f"https://{domain}{path}"
        logger.info(f"{method} {url}")
        auth = HTTPBasicAuth(user, token)
        headers = {
            "Accept": "application/json"
        }

        res = requests.request(
            method,
            url,
            headers=headers,
            params=query,
            auth=auth
        )

        if res.status_code != requests.codes.ok:
            return False

        return json.loads(res.text)
