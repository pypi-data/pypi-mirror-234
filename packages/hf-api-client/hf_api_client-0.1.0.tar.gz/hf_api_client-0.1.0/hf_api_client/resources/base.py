import json

from hf_api_client.utils import urljoin

class ResourcePool:
    def __init__(self, endpoint, session):
        self._endpoint = endpoint
        self._session = session

    def get_url(self):
        return self._endpoint

class CreatableResource:
    def create_item(self, item, params=None, files=None):
        if files:
            res = self._session.post(self._endpoint, data=item, params=params, files=files)
        else:
            res = self._session.post(self._endpoint, data=json.dumps(item), params=params)
        return res

class GettableResource:
    def fetch_item(self, code, params=None):
        url = urljoin(self._endpoint, code)
        res = self._session.get(url, params=params)
        return res

class ListableResource:
    def fetch_list(self, params=None):

        if not params:
            params = {}

        res = self._session.get(self._endpoint, params=params)
        return res

class UpdatableResource:
    def update_item(self, code, item, params=None):
        url = urljoin(self._endpoint, code)
        res = self._session.put(url, data=json.dumps(item), params=params)
        return res

class DeletableResource:
    def delete_item(self, code, params=None):
        url = urljoin(self._endpoint, code)
        res = self._session.delete(url, params=params)
        return res