import requests as rq

from hf_api_client import utils, resources


class Client:
    BASE_URL = 'https://api.endpoints.huggingface.cloud'

    def __init__(self, token, version='v2'):

        self._session = rq.Session()
        self._session.headers = {
            "Authorization": f"Bearer {token}"
        }

        self._base_url = utils.urljoin(
            self.BASE_URL, version
        )
        self._resources = {
            'provider': resources.QueryPool(
                utils.urljoin(
                    self._base_url, 'provider'
                ),
                self._session
            ),
            'endpoint': resources.EndpointPool(
                utils.urljoin(
                    self._base_url, 'endpoint'
                ),
                self._session
            )
        }

    @property
    def resources(self):
        return self._resources
    
    @property
    def provider(self):
        return self._resources['provider']
    
    @property
    def endpoint(self):
        return self._resources['endpoint']