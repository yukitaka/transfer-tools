import json
import os
import requests
from src.utils import store
from src.utils.logger import logger
from datetime import datetime, timezone
from requests.auth import HTTPBasicAuth

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
        domain = os.environ.get('CONFLUENCE_DOMAIN')
        user = os.environ.get('ATLASSIAN_USER')
        token = os.environ.get('ATLASSIAN_TOKEN')
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

    @staticmethod
    def store(filename, data):
        logger.info(filename)
        if not os.path.exists(filename):
            store.save_json(filename, data)

            return True

        if type(data) is dict and 'version' in data:
            mtime = datetime.fromtimestamp(os.stat(filename).st_mtime, tz=timezone.utc)
            if mtime < datetime.fromisoformat(data['version']['createdAt']):
                store.save_json(filename, data)

                return True
        else:
            store.save_file(filename, data)

            return True

        return False
