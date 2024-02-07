import os
import requests

class Base:
    @staticmethod
    def get_request(path, query=None, v=3):
        return Base.request('get', path, params=query, v=v)

    @staticmethod
    def post_request(path, json=None, data=None, files=None, v=3):
        return Base.request('post', path, json=json, data=data, files=files, v=v)

    @staticmethod
    def request(method, path, params=None, data=None, files=None, json=None, v=3):
        host = os.environ.get('GROWI_DOMAIN')
        url = f"{host}/_api"
        if v == 3:
            url += '/v3'
        url += path
        token = os.environ.get('GROWI_TOKEN')
        req = {"method": method, "url": url, "params": params}
        if data:
            data['access_token'] = token
            req["data"] = data
            req["files"] = files
        elif json:
            json["access_token"] = token
            req["headers"] = {"Content-Type": "application/json", "Accept": "application/json"}
            req["json"] = json
        else:
            req["headers"] = {"Content-Type": "application/json", "Accept": "application/json"}
            req["params"]["access_token"] = token

        print(req)
        res = requests.request(**req)
        if res.status_code != requests.codes.ok and res.status_code != requests.codes.created:
            print(res.text)
            return res.status_code

        return res.json()
