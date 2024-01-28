import os
import requests

class Base:
    @staticmethod
    def get(path, query=None, v=3):
        return Base.request('get', path, params=query, v=v)

    @staticmethod
    def request(method, path, params=None, data=None, json=None, v=3):
        host = os.environ['GROWI_DOMAIN']
        url = f"{host}/_api"
        if v == 3:
            url += '/v3'
        url += path
        token = os.environ['GROWI_TOKEN']
        req = {"method": method, "url": url, "params": params}
        if data:
            data["access_token"] = token
            req["headers"] = {"Content-Type": "multipart/form-data"}
            req["data"] = data
        elif json:
            json["access_token"] = token
            req["headers"] = {"Content-Type": "application/json"}
            req["json"] = json
        else:
            req["headers"] = {"Content-Type": "application/json"}
            req["params"]["access_token"] = token

        req['headers']['Accept'] = 'application/json'

        return requests.request(**req).json()
